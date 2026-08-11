---
title: Glossary
kind: reference
owner: role:editorial-lead
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal, public]
summary: "Every term the suite uses, in plain language, assuming no technical background."
---

# Glossary

Nothing here assumes you have read any code.

## The suite

**Atlas** — nine standards that say what must be true of a body of digital work,
plus a command that checks a repository against them.

**Standard** — one of the nine documents in `spec/`. Each answers one question.

**Rule** — one numbered requirement, such as `PJ-01`. The identifier is a
permanent address, so a review comment can cite it.

**Checklist item** — a gate that checks one or more rules at a maturity level,
such as `ID-02`. A rule says what is required; a checklist item says when.

**Gate** — one automated check. `atlas check` runs 24 of them.

**Profile** — a level of the checklist: Baseline, Beta, Production, Hardened.

**Waiver** — a recorded exception: the item, the reason, the approver, and an
expiry. Without the expiry it is not a waiver, it is a silence.

## The files

**Manifest** — a small file of declared facts. `project.yaml` says what this
repository is; `admin.yaml` says who may act.

**Front matter** — the block at the top of a document declaring its title, kind,
owner, status, and dates.

**Schema** — a machine-readable description of what a manifest may contain. It
turns a typo into a failed check.

**Lexicon** — the file recording how we spell our names and which phrasings we
have replaced.

**Design system** — the file recording the fleet's visual identity as named
tokens. Everything that draws derives its values from it; nothing forks it.

**Token** — one named visual value in the design system, such as a colour role
or a spacing step. The only legal source of a visual value.

## Classification

**Dimension** — one of the eight axes in MATRIX, `D1` to `D8`.

**Stage** — where a project is in its life, from `idea` to `archived`.

**Maturity** — how much anyone may lean on it, from `experimental` to
`hardened`. Independent of stage.

**Principal** — anything that can act: a person, a team, or an agent.

**Duty** — one of the six components of ownership: direction, code, operations,
security, cost, compliance.

## Work

**Workstream** — one initiative, as a numbered directory with nine sections.

**Task table** — the single place a workstream's status is recorded.

**Generated view** — a file a tool writes from another file. Editing one by hand
is always wrong; the next run overwrites it.

## Tooling

**CLI** — command-line interface. A program you run by typing its name.

**Exit code** — the number a command returns so a script can tell what happened:
`0` fine, `1` violations, `2` bad usage, `3` not found, `4` not a repository.

**CI** — continuous integration. The service that runs the checks automatically
when someone proposes a change.
