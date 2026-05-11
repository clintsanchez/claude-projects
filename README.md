# BlakSheep Marketing Assistant

The operating system for BlakSheep's weekly marketing output (BlakSheep brand + client work). Source of truth lives in this repo. Daily execution lives in Claude Projects.

## Structure

```
brand-bible.md              Master voice + positioning profile (BlakSheep)
voice-log.md                Running log of shipped pieces, sharpens voice over time
client-brand-briefs/        One file per client (created via client-brand-intake template)
templates/                  Master prompts for the 5 production templates + intake
weekly/                     Monday plan + Friday review rituals
```

## Setup (one-time, ~30 min)

1. Fill in `brand-bible.md` — replace every `TBD` with real content from the Phase 1-3 planning notes.
2. Create 5 Claude Projects on claude.ai, one per template:
   - Blog Post
   - LinkedIn Post
   - Service Page
   - Cold Outbound
   - Case Study
3. For each Project: paste the matching `templates/*.md` content into the **System Prompt** field.
4. For each Project: upload `brand-bible.md` and `voice-log.md` as **Project Knowledge** files.
5. Optionally create 2 more Projects for the weekly rituals (Monday Plan, Friday Review) using `weekly/*.md`.

## Daily/weekly flow

| When | What | Time |
|---|---|---|
| Monday AM | Run the Monday Plan project. Get the week's content list. | 15 min |
| Tue-Thu | Run the matching template project for each piece on the list. Edit, ship. | 5-10 pieces |
| Friday PM | Run the Friday Review project. Paste shipped pieces + responses. Add voice-log entries. | 10 min |

## Refreshing the system

- **Every Friday:** add 1-3 entries to `voice-log.md` for the best pieces that shipped that week. Re-upload `voice-log.md` to each Claude Project's knowledge.
- **Quarterly:** review the voice log + brand bible together. Update brand-bible.md if voice has evolved. Re-upload.
- **Per new client:** run the `client-brand-intake.md` template. Save output to `client-brand-briefs/[client-slug].md`. Create a Claude Project specifically for that client's work, with their brief as knowledge instead of brand-bible.

## Voice variable

Every production template accepts a `brand_voice` input:
- `BlakSheep` — use brand-bible.md as voice profile
- `client:[slug]` — use client-brand-briefs/[slug].md as voice profile

This is the single hinge that makes the system work for ~50/50 BlakSheep / client output.

## Branch

Active development: `claude/setup-marketing-assistant-nZVec`
