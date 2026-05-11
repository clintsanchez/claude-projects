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

## Visual generation (Canva integration)

Every production template (blog, LinkedIn, service page, case study) now outputs a **Visual Brief** at the bottom. The brief specifies every image slot the piece needs: subject, style, dimensions, alt text, and design notes.

You can take that brief in two directions:

### Option 1: Hand it off (no tools required)
Paste the Visual Brief to a designer, into Canva manually, into Midjourney/DALL-E/Adobe Firefly, or just shoot it yourself. The brief is the spec; the production happens wherever you already work.

### Option 2: Generate inline (Canva MCP tools)
Within a Claude session that has the Canva MCP server connected, ask: **"Generate the [slot name] visual using Canva."** Claude will:
1. Ask whether you want it on-brand (calls `list-brand-kits` and lets you pick a brand kit).
2. Call `generate-design` with the brief details translated into a Canva query.
3. Return design candidate options for you to pick from.
4. On your pick, call `create-design-from-candidate` to make it editable in your Canva account, then `export-design` to give you a PNG/JPG download URL.

**What works well on the Canva path:**
- Branded social graphics (LinkedIn images, pull-quote cards)
- Results charts (bar/line/before-after)
- Simple infographics
- Hero graphics for blog posts when illustrated, not photographic

**What still needs other tools or a designer:**
- Original photography (aircraft on a tarmac, executive headshots, client-site shots)
- Complex multi-source compositions
- Brand-defining hero imagery for the service pages

The templates flag these distinctions in their Generating the visuals notes.

## Branch

Active development: `claude/setup-marketing-assistant-nZVec`
