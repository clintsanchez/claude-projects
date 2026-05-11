# BlakSheep Marketing Assistant

Multi-client marketing operating system. One source of truth for voice + brand + visual assets, scalable across your full client roster. Daily execution in Claude Projects.

## Repo structure

```
brand-bible.md              BlakSheep's own voice + positioning
voice-log.md                Running log of shipped pieces (BlakSheep + all clients), sharpens voice over time

client-brand-briefs/        One markdown file per client (voice profile, ICP, content pillars)
  [client-slug].md

brand-templates/            One HTML file per client + a master reference
  _master.html              House design system — every client template inherits its slot structure
  [client-slug].html

templates/                  Master prompts
  blog-post.md              5 production templates
  linkedin-post.md
  service-page.md
  cold-outbound.md
  case-study.md
  client-brand-intake.md    Setup: one-time per new client (voice profile)
  brand-template-generator.md   Setup: one-time per new client (HTML brand template)

weekly/                     Weekly rituals
  monday-plan.md
  friday-review.md
```

## How it scales to many clients

Two files per new client:
- `client-brand-briefs/[slug].md` — voice profile (run client-brand-intake template, ~30 min)
- `brand-templates/[slug].html` — visual brand template (run brand-template-generator template, ~30-60 min first time, faster after)

That's it. **The Claude Projects don't multiply.** They load every client's brief and brand template as knowledge, and you tell them which client you're working on by setting `brand_voice: client:[slug]` as an input when you run a template.

## Setup (one-time, ~1 hour)

1. **Fill in `brand-bible.md`** — replace every TBD with BlakSheep's voice + positioning.

2. **Create `brand-templates/_master.html`** — your house design system in HTML with variants for: featured image, bar chart, pie chart, line chart, infographic, quote card, stat callout, comparison diagram, process diagram. (This is what the brand-template-generator adapts per client.)

3. **Create 9 Claude Projects** on claude.ai, one per template file:

| Project name | System prompt source | Purpose |
|---|---|---|
| Blog Post | `templates/blog-post.md` | Long-form authority content |
| LinkedIn Post | `templates/linkedin-post.md` | Short authority + distribution |
| Service Page | `templates/service-page.md` | Conversion page copy |
| Cold Outbound | `templates/cold-outbound.md` | Outbound emails + follow-ups |
| Case Study | `templates/case-study.md` | Client win writeups |
| Client Brand Intake | `templates/client-brand-intake.md` | New client voice profile setup |
| Brand Template Generator | `templates/brand-template-generator.md` | New client HTML brand template setup |
| Monday Plan | `weekly/monday-plan.md` | Weekly content planning |
| Friday Review | `weekly/friday-review.md` | Weekly retrospective + voice log |

4. **For each production project (top 5 + Monday Plan + Friday Review)**, upload as Project Knowledge:
   - `brand-bible.md`
   - `voice-log.md`
   - All `client-brand-briefs/*.md`
   - All `brand-templates/*.html`

5. **For setup tool projects (Client Brand Intake, Brand Template Generator)**, knowledge files vary — see each template for specifics.

## Adding a new client (~1-1.5 hours)

1. **Voice profile**: in the Client Brand Intake project, run the intake with the client's website copy, sample emails/posts, brand guide (if any), and kickoff call notes. Save output to `client-brand-briefs/[slug].md`. Commit.
2. **HTML brand template**: in the Brand Template Generator project, run the generator with the client's logo, brand colors, fonts, and 1-2 sample marketing pieces. Save output to `brand-templates/[slug].html`. Commit.
3. **Re-upload knowledge** to every production project so the new client is loaded.

That's the entire onboarding for client N+1. After 2-3 clients onboarded this way you'll find the bottleneck (probably the HTML template work the first time) and we can build a brand-template-generator that's smarter about extracting from sample pieces.

## Daily / weekly flow

| When | What | Time |
|---|---|---|
| Monday AM | Run Monday Plan. Get the week's content list across BlakSheep + clients. | 15 min |
| Tue-Thu | Run templates for each piece. Set `brand_voice: client:[slug]` per piece. Edit copy, render visuals, ship. | 5-10 pieces |
| Friday PM | Run Friday Review. Add voice-log entries. Re-upload `voice-log.md` to every project. | 10 min |

## Voice variable

Every production template accepts a `brand_voice` input:
- `BlakSheep` — uses `brand-bible.md` + `brand-templates/_master.html`
- `client:[slug]` — uses `client-brand-briefs/[slug].md` + `brand-templates/[slug].html`

This is the single hinge that makes the whole system multi-client without project sprawl.

## Visual asset workflow

Every production template that needs visuals outputs a **Visual Asset Plan** at the end of its output: a structured spec for 1 featured image + 4-9 supporting assets (images, charts, infographics, quote cards, stat callouts). Per asset:

- **Placement** — exact location in the piece (after section X)
- **Asset Type** — image | bar chart | pie chart | line chart | infographic | quote card | stat callout | comparison diagram | process diagram
- **Placeholder** — `[slugified-bracketed-name]` for the in-doc insertion marker
- **Filename** — `slugified-name-no-stop-words` (doubles as alt text)
- **Detailed Prompt** — cinematic/illustrative description for images; **real researched data with source citations** for charts/data viz

You take that spec → render against the client's `brand-templates/[slug].html` → export each to webp → drop into the published piece. The render step itself can be done by Claude once `brand-templates/_master.html` exists in the repo — we'll wire that up via `templates/visual-asset-render.md` (next).

**Why this format**: matches the asset spec process you already use elsewhere. Filenames-as-alt-text, structured placement, real data for charts, slugified placeholders for clean doc insertion.

## Refreshing the system

- **Every Friday**: add 1-3 voice-log entries from the best pieces that shipped. Re-upload `voice-log.md` to every project.
- **Per new client**: add 2 files (brief + template), re-upload knowledge to production projects.
- **Quarterly**: review the voice log + brand bible together. Update if voice has evolved. Audit client brand templates for drift after rebrands.

## Branch

Active development: `claude/setup-marketing-assistant-nZVec`
