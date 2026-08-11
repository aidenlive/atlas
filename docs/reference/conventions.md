---
title: Naming and placement conventions
kind: reference
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal, developers]
summary: "Where anything goes and what to call it, decided once so nobody decides again."
---

# Naming and placement conventions

## Files and directories

| Thing | Convention | Example |
|---|---|---|
| Repositories | `lowercase-hyphenated`, noun-first | `invoice-api` |
| Root documents | `SCREAMING_CASE.md` | `README.md`, `SECURITY.md` |
| Manifests | `lower.yaml` at the root | `project.yaml`, `admin.yaml` |
| Schemas | `<kind>.schema.json` | `project.schema.json` |
| Standards | `<id>.md`, matching the declared id | `spec/workspace.md` |
| Documents | `kebab-case.md` | `docs/guides/install.md` |
| Decisions | `NNNN-short-title.md` | `docs/decisions/0002-number-the-unnumbered.md` |
| Prompts | `request-<verb>-<object>.txt` | `request-cut-release.txt` |
| Workstreams | `NN_slug/` | `work/01_harden-repository-baseline/` |
| Source files | The language's idiom, absolutely | `snake_case.py`, `PascalCase.cs` |
| Workspace files | `date_what_context_version` | `2026-03-14_proposal_acme_v3.pdf` |

## Where things live

| If it is… | It goes in |
|---|---|
| A rule the organization must follow | `spec/` |
| How to do something | `docs/guides/` |
| A lookup, list, or table | `docs/reference/` |
| Why something is the way it is | `docs/decisions/` |
| Shared prompts, the design system, icons, typefaces, media | `library/` |
| Work in progress | `work/NN_slug/` |
| Deployment and infrastructure | `ops/` |
| A worked, validated sample | `examples/` |

## Identifiers

| Kind | Shape | Example |
|---|---|---|
| Principal | `person:` `team:` `role:` `agent:` plus a slug | `team:payments` |
| Rule | Namespace, then a number | `PJ-01`, `I-4`, `L-A1` |
| Workstream | Two digits, underscore, slug | `01_harden-repository-baseline` |
| Task | `T-` and a number, unique in its table | `T-04` |
| Requirement, criterion, milestone, issue | `R-` `C-` `M-` `I-`, local to a workstream | `C-02` |

Workstream-local identifiers carry no relationship to the specification
namespaces: `R-01` in a workstream is a requirement, not an ADMIN role rule.

## Branches, commits, versions

- Branches: `type/short-description` — `feat/webhook-retries`
- Commits: Conventional Commits — `feat:`, `fix:`, `docs:`, `chore:`
- Tags: `vX.Y.Z`; SemVer for anything with consumers, CalVer permitted for
  continuously deployed applications

## Dates

ISO (`2026-08-08`) in manifests, front matter, filenames, and tables. Long dates
(`8 August 2026`) in a sentence. Never a numeric format that means two different
days on two continents.
