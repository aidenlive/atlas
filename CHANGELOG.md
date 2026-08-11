# Changelog

All notable changes to Atlas. The release version and the standard's contract
version move independently — see
[docs/reference/versioning.md](docs/reference/versioning.md).

## [1.0.0] — 2026-08-10

The initial release.

### The standard

Nine standards, each answering one question of a body of digital work, with
211 permanently identified rules and checklist items between them:

WORKSPACE (where does a file live?), PROJECT (what must be true inside a
repository?), MATRIX (what kind of project is it?), CHECKLIST (is it good
enough?), ADMIN (who may act, who answers, who pays?), PRESENTATION (how does
it show itself?), LIBRARY (where do shared assets live, and on what terms?),
WORKSTREAM (what work is happening, by whom, and is it done?), and WRITING
(how is any of this written?).

Exceptions are waivers in `project.yaml` — named, reasoned, approved, and
expiring — never exclusion lists in the tooling.

### The tooling

- **`atlas check`**: 24 named gates over manifests, structure, documents, the
  library, work, and prose; every failure cites the rule behind it.
- **`atlas lint`**: a prose linter with 11 rules from WRITING, reading the
  organization's lexicon so a naming decision is enforced everywhere at once.
- **`atlas init`**, **`status`**, **`doctor`**, **`validate`**, **`spec`**,
  **`prompt`**, **`library`**, **`work`**, **`site`**, and **`completion`** —
  one command per thing a person does with a repository. Every command takes
  `--json`; the reference is generated from the argument parser.

### The library

- 78 written-once prompts across 14 lifecycle categories, each asking for one
  thing, with guardrails in the sentence for anything destructive.
- **Neue v1.0**, the fleet's design system: normative OKLCH tokens as front
  matter in `library/design/DESIGN.md`, application prose after them. The
  badges, terminal demos, and rendered site all derive from it.
- The **`neue-design`** skill in `library/skills/`: the identity as applicable
  material — built CSS, a behaviour layer, five layouts, four document
  templates, a gallery, and a starter.
- The lexicon: the names the organization spells one way, enforced by the
  linter.

### The repository

- A starter template that passes every gate on its first scaffold, presenting
  the same skeleton, badge row, and recorded terminal demo the root does.
- Every generated view — indexes, dashboards, badges, screenshots, counts, the
  CLI reference — is derived by a script and held current by CI.
- CI runs the suite against this repository itself; the standard eats first.
- The rendered site deploys to GitHub Pages on every push to `main`.
