# Brand Templates

One HTML brand template per client (plus a master reference). The visual asset workflow renders each Visual Asset Plan against the matching client template to produce branded HTML files, which then export to webp.

## Files

```
_master.html                  House design system. Reference template every client template inherits structure from.
[client-slug].html            One file per client. Same slot structure as _master, different colors/fonts/logo.
```

## Asset variants every template must define

Each brand template defines a set of **asset variants** matching the Visual Asset Plan's asset types:

| Variant | Use case |
|---|---|
| `featured-image` | Hero with title overlay (blog post, case study, service page) |
| `bar-chart` | Categorical comparisons |
| `pie-chart` | Composition / share |
| `line-chart` | Trends over time |
| `infographic` | Multi-step framework (3-7 steps) |
| `quote-card` | Pull-quote with attribution |
| `stat-callout` | Single big number + supporting text |
| `comparison-diagram` | Before/after, 2-column |
| `process-diagram` | Numbered steps (3-5) |

Each variant is parameterized — when an asset is rendered, the variant's text/data slots are filled in from the Visual Asset Plan's detailed prompt.

## Adding a new client template

Use the Brand Template Generator template (`templates/brand-template-generator.md`):
1. Feed it the client's logo, brand colors, fonts, and sample marketing pieces.
2. Save the output here as `[client-slug].html`.
3. Commit.

## When to refresh a template

- Client rebrands → regenerate.
- New asset variant added to `_master.html` → propagate (regenerate or hand-patch each client template).
- Quarterly: verify all client templates still match the client's current brand.

## TODO: `_master.html`

The master template is the next thing to land. Once it exists, the `templates/visual-asset-render.md` template can be wired up to read it and produce populated HTML per asset.
