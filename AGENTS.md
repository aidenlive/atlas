# Agent guide

The canonical instruction file for every AI agent working in this repository.
`CLAUDE.md` and `GEMINI.md` are stubs pointing here: vendors multiply, truth
must not (`PJ-11`).

## Purpose

Atlas is nine standards for organizing digital work — filesystems, repositories,
classification, quality, authority, presentation, shared assets, work, and
writing — plus the tooling that checks a repository against them. This
repository is self-hosting: it passes the standard it defines.

## Map

| Path | Holds |
|---|---|
| `spec/` | The nine standards and their JSON Schemas — the product |
| `src/atlas/` | The tooling: `core/` is a library, `cli/` is a thin layer on it |
| `library/` | Shared assets: 78 prompts, the design system, the skills, the lexicon |
| `work/` | Initiatives as numbered workstreams, with a generated dashboard |
| `template/` | The starter repository, which passes every gate on first run |
| `docs/` | Guides, reference, architecture, decisions |
| `project.yaml` | What this project is, in Matrix terms |
| `admin.yaml` | Who may act, and who answers |

## Commands

```bash
scripts/atlas check          # the repository against the standard, 24 gates
scripts/atlas lint --changed # prose this branch touched
python -m pytest tests/ -q   # the test suite
scripts/atlas work sync      # regenerate the dashboard after editing tasks
```

## Conventions

Naming, placement, branches, and commits follow
[`docs/reference/conventions.md`](docs/reference/conventions.md). Terminology
comes from [`library/lexicon/terms.yaml`](library/lexicon/terms.yaml); do not
invent a second spelling for anything. Cite rules by identifier (`PJ-01`), never
by section.

## Constraints

- **You may draft, edit, and review. You may not approve.** `R-3` caps an agent
  at `maintainer`: an agent can do a maintainer's work, but accountability is a
  human property.
- **Propose before you remove.** Deleting, overwriting, deprecating, or
  migrating anything means proposing a plan and waiting for a person.
- **Never edit a generated file.** `docs/reference/cli.md`,
  `library/prompts/index.yaml`, `library/design/index.yaml`,
  `work/README.md`, `work/index.yaml`, and everything under `assets/` are
  derived. Change the source, re-run the script.
- **Status lives in the task table** of the relevant workstream, nowhere else.
- **A rule change travels as one change-set**: prose, schema, standard version,
  changelog entry. Never ship one part alone.

## Definition of done

`atlas check` passes, `atlas lint` reports no errors, `pytest` passes, generated
files are current, the changelog has an entry, and the workstream that prompted
the change records the evidence in `07_validation/`.

## Pointers

- Start here: [`docs/reference/quick-reference.md`](docs/reference/quick-reference.md)
- Terms in plain language: [`docs/reference/glossary.md`](docs/reference/glossary.md)
- Why things are the way they are: [`docs/decisions/`](docs/decisions/0001-gates-as-a-registry.md)
