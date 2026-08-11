# neue-design

Apply **Neue v1.0**, the fleet's visual identity, to any web surface. The skill
is self-contained (`L-S2`): copy the directory, open `starter.html`, and build.

## What it produces

A page that inherits the fleet identity without naming a colour, a font size,
or a shadow directly. Every value resolves to a token in
[`library/design/DESIGN.md`](../../design/DESIGN.md), the normative source this
skill's CSS is built from (`L-A4`, `P-11`). Typefaces are DM Sans and
JetBrains Mono, loaded by the host page.

## What it contains

| Path | Is |
|---|---|
| `dist/neue.tokens.css` | The design tokens as CSS custom properties, light base, `[data-theme="dark"]` overrides |
| `dist/neue.css` | The component and layout classes (`n-*`, `t-*`), consuming tokens only |
| `dist/neue.js` | The behaviour layer: theme toggle, nav scroll shadow, disclosure controls |
| `layouts/` | Five page shells: dashboard, docs, settings, admin, auth |
| `templates/` | Four document templates: report, one-pager, email, social card |
| `gallery.html` | Every component, rendered — the visual reference |
| `starter.html` | A blank, wired page to copy from |

## How to apply it

1. Include, in order: `dist/neue.tokens.css`, `dist/neue.css`, `dist/neue.js`.
2. Start from `starter.html` or the closest file in `layouts/`.
3. Use only `n-*` component classes and `t-*` type classes; never write a hex,
   a px font size, or a shadow. If a value is missing, it is a token request
   against `DESIGN.md`, not a local override.
4. Theme with `data-theme="dark"` on `<html>`; density with `data-density`.

## Constraints

- The CSS here is **built output**. A visual change starts in
  `library/design/DESIGN.md` and is rebuilt; editing `dist/` forks the identity
  (`P-11`) and will be overwritten.
- One capability only (`L-S3`): this skill styles surfaces. Content, copy, and
  information architecture belong to WRITING and the templates' own guidance.
