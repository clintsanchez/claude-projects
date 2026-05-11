#!/usr/bin/env python3
"""Trash bulk-sender threads from the Gmail inbox.

A 'bulk sender' is any message whose headers include `List-Unsubscribe`
(RFC 2369) or `Precedence: bulk|list|junk` (RFC 3834). These are the
machine-generated marketing / notification / list emails that pile up.

By default the script is a dry run: it prints a per-sender report and
exits without modifying anything. Pass `--apply` to actually move the
matching threads to Trash.

Setup
-----
1. Create an OAuth desktop client in the Google Cloud console and download
   the credentials JSON to `credentials.json`.
2. Enable the Gmail API on the same project.
3. `pip install -r requirements.txt`
4. `python gmail_cleaner.py`            # dry run
   `python gmail_cleaner.py --apply`    # trash bulk threads
"""

from __future__ import annotations

import argparse
import collections
import os
import sys
from email.utils import parseaddr

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
BULK_PRECEDENCE = {"bulk", "list", "junk"}


def authenticate(credentials_path: str, token_path: str):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def list_inbox_threads(service, query: str, max_threads: int):
    threads, page_token = [], None
    while len(threads) < max_threads:
        resp = (
            service.users()
            .threads()
            .list(
                userId="me",
                q=query,
                maxResults=min(500, max_threads - len(threads)),
                pageToken=page_token,
            )
            .execute()
        )
        threads.extend(resp.get("threads", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return threads


def thread_is_bulk(service, thread_id: str):
    """Return (sender_email, subject) if the thread looks bulk, else None."""
    msg = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=thread_id,
            format="metadata",
            metadataHeaders=["From", "Subject", "List-Unsubscribe", "Precedence"],
        )
        .execute()
    )
    headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
    is_bulk = "list-unsubscribe" in headers or headers.get("precedence", "").lower() in BULK_PRECEDENCE
    if not is_bulk:
        return None
    _, sender = parseaddr(headers.get("from", ""))
    return sender.lower(), headers.get("subject", "(no subject)")


def trash_thread(service, thread_id: str):
    service.users().threads().trash(userId="me", id=thread_id).execute()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="Actually move threads to Trash (default: dry run).")
    parser.add_argument("--query", default="in:inbox", help="Gmail search to scan (default: in:inbox).")
    parser.add_argument("--max", type=int, default=500, dest="max_threads", help="Max threads to scan (default: 500).")
    parser.add_argument("--credentials", default="credentials.json", help="Path to OAuth client secrets.")
    parser.add_argument("--token", default="token.json", help="Path to cached user token.")
    args = parser.parse_args()

    try:
        service = authenticate(args.credentials, args.token)
    except FileNotFoundError:
        print(f"error: {args.credentials} not found. See module docstring for setup.", file=sys.stderr)
        return 2

    threads = list_inbox_threads(service, args.query, args.max_threads)
    print(f"scanning {len(threads)} thread(s) matching '{args.query}'...")

    by_sender: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for t in threads:
        try:
            result = thread_is_bulk(service, t["id"])
        except HttpError as e:
            print(f"  skip {t['id']}: {e}", file=sys.stderr)
            continue
        if result:
            sender, subject = result
            by_sender[sender].append((t["id"], subject))

    if not by_sender:
        print("no bulk senders found.")
        return 0

    total = sum(len(v) for v in by_sender.values())
    print(f"\nfound {total} bulk thread(s) from {len(by_sender)} sender(s):\n")
    for sender, items in sorted(by_sender.items(), key=lambda kv: -len(kv[1])):
        print(f"  {len(items):4d}  {sender}")

    if not args.apply:
        print("\ndry run — re-run with --apply to move these threads to Trash.")
        return 0

    print("\ntrashing...")
    trashed = failed = 0
    for sender, items in by_sender.items():
        for thread_id, _subject in items:
            try:
                trash_thread(service, thread_id)
                trashed += 1
            except HttpError as e:
                failed += 1
                print(f"  failed {sender} {thread_id}: {e}", file=sys.stderr)
    print(f"done. trashed={trashed} failed={failed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
