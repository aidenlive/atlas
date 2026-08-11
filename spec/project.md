---
id: project
order: 2
title: PROJECT
tagline: "An open standard for organizing software projects and repositories"
question: "What must be true inside a repository?"
version: "1.0"
status: stable
rule_prefixes: [PJ-]
checklist_prefixes: []
companions: [workspace, matrix, checklist, admin, presentation, library, writing]
kind: standard
owner: role:standards-maintainer
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers, public]
summary: "The closed root, the required documents, the manifest, and the agent guide that make a repository operable by a stranger."
---

# PROJECT: what must be true inside a repository

> A workspace organizes your *files*. A project organizes your *intent*.
> WORKSPACE tells you where a repository lives. PROJECT tells you what must be
> true inside it.

## What this is

PROJECT is the repository-level companion to [WORKSPACE](workspace.md). It
governs the universe inside a repository root: its structure, its documents, its
lifecycle, and its conventions.

Three convictions run underneath it.

**Repositories rot from the root.** Every stray file at the top level lowers the
cost of the next one. The root is the first screen a stranger and an agent both
see, so it is a closed set, not a suggestion.

**Agent-first is human-first.** Everything an AI agent needs — one code root, a
computable test path, a manifest at a fixed path, one canonical guide — is what a
new hire needed all along. Writing it down for the machine is how it finally gets
written down.

**Git is the archive.** In-repository graveyards (`legacy/`, `old/`,
`@removal-safe/`) are banned. Version control already keeps every deleted file
perfectly; a copy beside the live tree only poisons search, grep, and agents.

## The lifecycle

```text
idea ──▶ incubating ──▶ active ──▶ maintenance ──▶ deprecated ──▶ archived
```

Stages move rightward only. A revival is a *new* `active` declaration — an event
worth a changelog entry, not a silent edit. The enum and its transition matrix
are recorded in [MATRIX](matrix.md) `D2`.

## Root documents

Required in every repository past `idea`:

| File | Single job |
|---|---|
| `README.md` | Orient a stranger in 60 seconds |
| `LICENSE` | Legal terms. No license means not shippable |
| `CHANGELOG.md` | What changed, when, for whom (Keep a Changelog) |
| `AGENTS.md` | Everything an agent needs to operate |
| `CONTRIBUTING.md` | How change happens here |
| `project.yaml` | Machine-readable classification and status |

Conditionally required: `SECURITY.md` for anything deployed or published;
`CODE_OF_CONDUCT.md` for public projects accepting community contribution;
`ROADMAP.md` only if it is genuinely maintained; one vendor agent stub per agent
tool actually used.

Explicitly rejected: `INFO.md` and per-effort `XYZ-STATUS.md`. Both duplicate
truth that already has a home — the snapshot belongs in `README.md` and
`project.yaml`, active status belongs in the tracker, where it has an owner and a
state machine. A rotten status file is misinformation with authority.

## The canonical tree

```text
repo/
├── README.md  LICENSE  CHANGELOG.md  AGENTS.md  CONTRIBUTING.md  project.yaml
├── CLAUDE.md  GEMINI.md          ← stubs pointing at AGENTS.md
├── src/         ← the product. all shipped code. one importable root.
├── tests/       ← all automated tests, mirroring src/ topology
├── docs/        ← architecture/ decisions/ guides/ reference/ assets/
├── work/        ← initiatives as numbered workstreams (WORKSTREAM)
├── examples/    ← runnable, CI-verified usage samples
├── scripts/     ← dev and maintenance automation (not shipped)
├── ops/         ← deployment: containers, IaC, manifests, pipelines
├── assets/      ← images, fonts, brand, fixtures
├── library/     ← shared assets: prompts, icons, typefaces, media (LIBRARY)
├── .github/     ← CI workflows, templates, CODEOWNERS, settings as code
└── [dotfiles]   ← formatter, linter, and build configuration
```

`work/` and `library/` are **conditional roots**: they appear when the
repository uses the companion standard that defines them, and are absent
otherwise. Conditional does not mean improvised — where present, their internal
shape is fully specified by that standard.

## The rules

- **PJ-01 The root is a closed set.** Only the documents and directories named
  above may sit at the repository root. Anything else is a violation, not a
  preference.
- **PJ-02 Required documents exist past `idea`.** `README.md`, `LICENSE`,
  `CHANGELOG.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `project.yaml`.
- **PJ-03 Status files are rejected.** No `INFO.md`, no `XYZ-STATUS.md`. The
  snapshot lives in the README and the manifest; live status lives in the
  tracker.
- **PJ-04 The README follows the fixed skeleton.** Name and one-line value
  proposition, badges, what and why, quickstart, documentation links, status,
  contributing and license. Sections may be short; they may not be absent.
- **PJ-05 The quickstart is true.** A stranger on a clean machine reaches first
  success by copy-paste alone, or the quickstart is a bug report.
- **PJ-06 One source root.** All shipped code under `src/`, or the ecosystem's
  idiomatic equivalent. Monorepos use `packages/<name>/`, each itself
  PROJECT-shaped: the standard is fractal.
- **PJ-07 Tests mirror source topology.** The test for any file sits at a
  computable path, which turns "is this covered?" into a script.
- **PJ-08 Decisions are append-only.** ADRs in `docs/decisions/` are dated,
  numbered `NNNN-short-title.md`, and immutable once accepted. You supersede an
  ADR; you never edit one.
- **PJ-09 No in-repository graveyards.** No `legacy/`, `old/`, `deprecated/`, or
  `@removal-safe/`. Git is the archive. Any exception is a dated, scoped
  decision record with a deletion deadline.
- **PJ-10 Examples run in CI, or they are deleted.** An example that does not run
  is documentation that lies with confidence.
- **PJ-11 One canonical agent guide, many pointers.** `AGENTS.md` carries the
  seven sections: purpose, map, commands, conventions, constraints, definition of
  done, pointers. Vendor files are stubs of three lines or fewer that redirect to
  it. Vendors multiply; truth must not.
- **PJ-12 The manifest sits at a fixed path.** `project.yaml` at the root,
  schema-valid, with all eight MATRIX dimensions classified.
- **PJ-13 Ecosystem idiom inside `src`, the standard everywhere else.**
  Repositories `lowercase-hyphenated` and noun-first; directories plural
  for collections and singular for roles; docs `kebab-case.md`; branches
  `type/short-description`; commits Conventional Commits; tags `vX.Y.Z`.
- **PJ-14 Deprecation names a successor and a date.** Entering `deprecated`
  requires both, even when the successor is explicitly "none".
- **PJ-15 Change flows through review past `incubating`.** Branch, pull request,
  green CI, review, merge. Direct pushes to the default branch are disabled by
  branch protection: the rule is mechanical, not cultural.
- **PJ-16 Enforceable rules are enforced.** If a formatter, linter, or CI job can
  check a rule, it must. Prose is the fallback, never the mechanism.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| A root that grew | Every stray file lowers the cost of the next; violates `PJ-01` |
| `legacy/` beside `src/` | Two answers to "which is real?"; violates `PJ-09` |
| A README with no quickstart | Adoption cost paid by every reader forever; violates `PJ-05` |
| Per-vendor agent files that disagree | Truth forked across vendors; violates `PJ-11` |
| A manifest nobody validates | Classification that drifts silently; violates `PJ-12` |

## Related

- [WORKSPACE](workspace.md) — where the repository itself lives
- [MATRIX](matrix.md) — the vocabulary the manifest uses
- [CHECKLIST](checklist.md) — when it is good enough
- [PRESENTATION](presentation.md) — how it shows itself
