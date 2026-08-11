---
id: presentation
order: 6
title: PRESENTATION
tagline: "The repository presentation standard: metadata, README composition, and visual identity"
question: "How does it show itself?"
version: "1.0"
status: stable
rule_prefixes: [P-]
checklist_prefixes: [PR-]
companions: [project, matrix, checklist, library, writing]
kind: standard
owner: role:standards-maintainer
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers, public]
summary: "Forge metadata declared in the manifest, a fixed README order, and badges that cannot disagree with the truth."
---

# PRESENTATION: how it shows itself

> A repository's landing view is its user interface.
> Structure makes a repository operable; presentation makes it *adoptable*.
> Both are engineering, and both are checkable.

## What this is

PRESENTATION governs the first ten seconds of contact, long before anyone opens
`docs/`. It makes the same bet as the rest of the suite: **declared beats
configured.** Metadata typed into a settings page is unreviewable state; metadata
declared in the manifest and applied by tooling is a diff.

Where [WRITING](writing.md) governs how the prose reads, PRESENTATION governs
what surrounds it: the description, the hero, the badges, the order.

## Forge metadata

Every repository past `idea` declares, in `project.yaml`, the fields its listing
renders:

```yaml
metadata:
  description: "One sentence, ≤ 160 chars, value-first, no trailing period"
  website: https://example.dev
  topics: [kebab-case, three-to-ten, of-them]
```

- **P-01 Description.** Required, at most 160 characters, stating *value* rather
  than implementation. `Validates fleet manifests in CI`, not `A Python repo with
  some scripts`. It is the same sentence as the README's title line: one truth,
  two views.
- **P-02 Hero visual.** The README opens with a visual before any prose, shipped
  in light and dark variants behind `<picture>` with `prefers-color-scheme`. A
  dark-only banner is unreadable for half the audience. SVG preferred —
  versionable, diffable, no binary churn — and every image carries meaningful
  alt text, because the hero must degrade to words.
- **P-03 Topics.** Three to ten, kebab-case. The first is the MATRIX family; the
  rest are terms a searcher would actually type.
- **P-04 Website.** Required for `visibility: public`. A placeholder pointing at
  `docs/` is acceptable and honest; a broken link is not.
- **P-05 Settings as code.** Forge metadata is applied *from* the manifest, never
  hand-typed. Drift between manifest and forge is a defect, exactly as in ADMIN.

## README composition

The `PJ-04` skeleton gains a fixed visual order:

```text
1. Hero visual        (P-02, with alt text)
2. # Name — one-line value proposition   (identical to metadata.description)
3. Badge row          (rendered from project.yaml, never hand-drifted)
4. ## What & Why      (three sentences at most)
5. ## Quickstart      (copy-paste true)
…then Documentation, Status, Contributing, License.
```

- **P-06 One screen to comprehension.** Items 1 to 5 fit in the first viewport of
  a default render. Everything below the fold is elaboration.
- **P-07 Badges are views, not facts.** Every badge value is derivable from
  `project.yaml` or from CI. A badge that can disagree with the manifest is a
  second source of truth, and therefore banned.
- **P-08 Architecture is drawn.** Any repository with more than one moving part
  carries a diagram of the parts and their relations. Diagrams as code, so the
  diff reviews like prose.

## Fleet consistency

- **P-09 One shape everywhere.** Every repository presents the same skeleton:
  same root set, same README order, same `docs/` substructure, same badge row. A
  reader who has seen one repository has seen the navigation of all of them.
  Content varies by type; composition does not.
- **P-10 Names align across layers.** Repository name, manifest `name`, README
  title, and published artifact name agree. Renames are release events with
  redirects and a changelog entry.
- **P-11 Visual identity is inherited.** Fleet brand assets live once and are
  consumed, never forked. A fleet with fifty hand-made banners has no brand; it
  has fifty.

## Checklist additions

| ID | Profile | Item |
|---|---|---|
| ☐ **PR-01** | Baseline | `metadata:` block present and schema-valid (`P-01`, `P-03`, `P-04`) |
| ☐ **PR-02** | Baseline | README opens with a hero visual carrying alt text (`P-02`) |
| ☐ **PR-03** | Beta | Forge metadata applied from the manifest; no drift (`P-05`) |
| ☐ **PR-04** | Beta | Badge row present, values derivable from manifest or CI (`P-07`) |
| 🧭 **PR-05** | Production | First README screen passes `P-06` on a default render, reviewer-attested |
| ☐ **PR-06** | Production | Architecture diagram exists for multi-part repositories (`P-08`) |

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| The blank storefront | No description, no topics: invisible to the search that would have found it |
| The wall of text | Readers triage visually; the hero and badge row are the triage interface |
| Screenshot rot | A hero three versions old is misinformation with authority — regenerate it from the real thing |
| Badge cosplay | Static badges hand-set to green are decoration pretending to be evidence |
| Fifty brands | Per-repository improvisation; spend the creativity on the product |

## Related

- [PROJECT](project.md) — the README skeleton this extends
- [LIBRARY](library.md) — where inherited brand assets live
- [WRITING](writing.md) — how the sentences inside the shape are written
