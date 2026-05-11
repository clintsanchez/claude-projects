# Brand Templates

One HTML brand template per client (plus a master reference, dark + light modes). The visual asset workflow renders each Visual Asset Plan against the matching client template to produce branded HTML files, which then export to webp.

## Files

```
_master.html                                  House design system (dark mode). Primary reference.
_master-light.html                            Light mode variant of the master.
examples/                                     Reference assets (finished, not slot templates)
  featured-image-trash-can-cleaning-website.html
[client-slug].html                            One per client. Inherits master's variant structure, swaps colors/fonts/logo.
```

## Variant inventory (as of 2026-05-11)

All 10 variants present in both `_master.html` (dark) and `_master-light.html` (light):

| Variant ID | Pack | Asset Type | Notes |
|---|---|---|---|
| `deployment-hero` | Pack 01 | Featured Image / Hero | Full-width hero with badge + headline + subhead + 2 CTAs + logo seal. |
| `bar-chart` | Pack 02 | Bar Chart | "Fluff vs Reality" comparison-flavored. 4 bars with labels/values. |
| `portfolio-mockup` | Pack 03 | (custom) | 2-col: text side + device mockup. Showcasing finished work. |
| `quote-card` | Pack 04 | Quote Card | Testimonial-style with 5-star + quote + attribution. |
| `process-diagram` | Pack 05 | Process Diagram | 4-phase grid (Consult / Design / Deploy / Dominate). |
| `pie-chart` | Pack 06 | Pie Chart | Composition/share. Conic-gradient pie with legend + center stat. |
| `line-chart` | Pack 07 | Line Chart | Time-series trend with BlakSheep vs. Industry comparison line. Headline stat (e.g. +247%) and labeled axes. |
| `infographic` | Pack 08 | Infographic | 5-component grid with numbered tiles, icons, and the green-accent "winning component" highlighted. |
| `stat-callout` | Pack 09 | Stat Callout | Single huge number (160px green) + eyebrow + headline + cited source. |
| `comparison-diagram` | Pack 10 | Comparison Diagram | True 2-col WITHOUT/WITH with VS center pill, X/check iconography. |

Additional finished example in `examples/featured-image-trash-can-cleaning-website.html` — an alternate `featured-image` style with phone-mockup + photo background overlay. Reference for a more layered hero treatment.

## Slot system

Variants 6-10 use `data-slot="..."` attributes on every replaceable element to make programmatic rendering deterministic. Slot names per variant:

- `pie-chart`: `pie-slice-{1,2,3}-{label,value}`, `pie-conic-gradient`, `pie-center-{value,label}`
- `line-chart`: `line-subhead`, `line-headline-{stat,label}`, `line-svg`
- `infographic`: `infographic-{count,count-label}`, `infographic-item-{1..5}`
- `stat-callout`: `stat-{eyebrow,number,headline,context,source}`
- `comparison-diagram`: `comparison-{subhead,without-column,with-column}`

The render templates (`templates/visual-asset-render.md`) populate these slots from the Visual Asset Plan's detailed prompts.

Variants 1-5 (the originals from your upload) don't use `data-slot` markers — they rely on the render template to identify replaceable text by position. We can retro-add slots to 1-5 later if rendering accuracy needs it.

## Brand specs embedded in `_master.html`

| Element | Value |
|---|---|
| Brand Green | `#61CE70` |
| Brand Moss | `#2C3B38` |
| Brand Charcoal (dark) | `#1A1A1A` |
| Brand Charcoal (light) | `#2F2F2F` |
| Brand Slate (dark) | `#94A3B8` |
| Brand Slate (light) | `#707E92` |
| Heading font | Poppins 700/800/900, uppercase, tight letter-spacing |
| Body font | Open Sans 400/700 |
| Logo URL | `https://blaksheepcreative.com/wp-content/uploads/2023/01/blaksheep-creative-denham-springs-green-white-logo.svg` |
| Container width | 781px (master) / 1000px (featured image example) |
| Signature motifs | Tactical blueprint grid overlay; logo seal (moss circle, green border, bottom-right); brand badges (green pill or moss-on-green); italic subhead with green left border; all-caps headline with one accent word in green. |

These specs are reflected in `brand-bible.md` section 6 (Visual identity).

## Adding a new client template

Use `templates/brand-template-generator.md`:
1. Feed it the client's logo, brand colors, fonts, and sample marketing pieces.
2. Save the output here as `[client-slug].html`.
3. Commit.

The generator inherits the variant slot structure from `_master.html`. Same variants, swapped brand values.

## When to refresh a template

- Client rebrands → regenerate that client's template.
- Master template gets a new variant → propagate to client templates (regenerate or hand-patch).
- Quarterly: verify all client templates still match the client's current brand.

## Mode selection

Per-piece, decide dark vs. light:
- Default to `_master.html` (dark) for tactical, high-contrast pieces (case studies, performance content, social-first).
- Use `_master-light.html` for editorial-feeling content (blog hero images for SEO, longer-form authority pieces, service pages).

The render templates currently default to dark unless the user specifies `mode: light` in the Visual Asset Plan inputs.
