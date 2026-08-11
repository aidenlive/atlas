# library

Shared assets, made first-class artifacts rather than attachments somebody still
has (LIBRARY).

| Directory | Holds |
|---|---|
| [`prompts/`](prompts/README.md) | 78 written-once requests across 14 categories |
| [`design/`](design/README.md) | Neue, the fleet's design system: tokens and application prose |
| [`skills/`](skills/README.md) | Agent skills: packaged capabilities, one directory per skill |
| [`lexicon/`](lexicon/terms.yaml) | The names this organization spells one way, and the phrasings it replaced |

All four are read by the tooling: `atlas prompt` and `atlas library` read the
prompts and skills, everything that draws derives from the design system, and
`atlas lint` reads the lexicon. A change here changes what the checks enforce
and what the artifacts look like.

Icons, typefaces, and media have their rules in
[`spec/library.md`](../spec/library.md) (`L-I`, `L-T`, `L-M`) and their
directories appear when a repository holds them.
