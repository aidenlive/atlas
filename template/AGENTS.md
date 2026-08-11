# Agent guide

The canonical instruction file for every AI agent working here. Vendor files are
stubs that point at this one (PJ-11).

## Purpose

{{DESCRIPTION}}

## Map

| Path | Holds |
|---|---|
| `src/` | All shipped code, one importable root |
| `tests/` | Automated tests, mirroring `src/` |
| `docs/` | Architecture, decisions, guides, reference |
| `work/` | Initiatives as numbered workstreams |
| `project.yaml` | What this project is, in Matrix terms |
| `admin.yaml` | Who may act, and who answers |

## Commands

```bash
atlas check          # this repository against the standard
atlas lint --changed # prose you touched
atlas work sync      # regenerate the work dashboard after editing tasks
```

## Conventions

Naming, branches, and commits follow [CONTRIBUTING.md](CONTRIBUTING.md). Where
this repository adopts a lexicon, terminology comes from it; either way, do not
invent a second spelling for anything.

## Constraints

- Propose a plan before deleting, overwriting, or migrating anything.
- Never edit a generated file: `work/README.md`, `work/index.yaml`, and anything
  marked generated at the top.
- Record status in the task table of the relevant workstream, and nowhere else.
- You may draft, edit, and review. You may not approve: ADMIN `R-3` caps an
  agent at `maintainer`, and accountability is a human property.

## Definition of done

`atlas check` passes, tests pass, the changelog has an entry, and the work
that prompted the change is recorded in its workstream.

## Pointers

- The standards: <https://github.com/OWNER/atlas>
- This project's decisions: `docs/decisions/`
