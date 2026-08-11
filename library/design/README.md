# library/design

The fleet's visual identity, as one first-class asset (`P-11`, `L-A1`).

| File | Is |
|---|---|
| [`DESIGN.md`](DESIGN.md) | **Neue v1.0** — the design system. Normative YAML front matter (tokens, regions, shells, components), then the prose for applying them |
| `index.yaml` | This class's machine index, generated (`L-A2`) |

## How it is consumed

The front matter is normative: if a value appears on a screen, it resolves to a
token in that file, and `{group.token}` references resolve at build time. In
this repository three things consume it, and none of them names a colour
directly:

| Consumer | Via |
|---|---|
| The README badges | `scripts/build_design.py` → `assets/design/tokens.yaml` → `build_assets.py` |
| The terminal demos | The same tokens → `build_screenshots.py` |
| The rendered site | The same tokens → `atlas site build` |

The `design-current` gate holds the chain together: the file must parse, every
reference must resolve, and the derived tokens must match a regeneration. A
drawn artifact that disagrees with its source is the visual form of a badge that
disagrees with the manifest (`P-07`).

## Changing it

Edit `DESIGN.md`, then:

```bash
python scripts/build_design.py
python scripts/build_assets.py
python scripts/build_screenshots.py
```

Downstream repositories consume this file — through their own token build or by
reading it — and never fork it. A fleet with fifty hand-made palettes has no
identity; it has fifty (`P-11`).
