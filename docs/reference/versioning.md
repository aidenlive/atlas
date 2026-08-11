---
title: Versioning
kind: reference
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal, developers]
summary: "Two numbers that move independently, and why conflating them causes trouble."
---

# Versioning

Atlas carries two version numbers. They are not the same number and they do not
move together.

| Number | Example | Answers |
|---|---|---|
| Release version | `1.0.0` | Which build of the tooling is this? |
| Standard version | `project/1.0` | Which contract is the repository written against? |

## The release version

Ordinary semantic versioning for the `atlas-standard` package.

- **Patch** — a bug fix in a gate, or a clearer message
- **Minor** — a new command, flag, or gate that nothing previously relied on
- **Major** — a removed command or flag, or a changed exit code

## The standard version

The contract every repository declares in `project.yaml`. It moves only when
what is *required* changes.

- **Minor** (`1.0` → `1.1`) — rules added, or relaxed. A repository that passed
  before still passes.
- **Major** (`1.x` → `2.0`) — a rule tightened or removed. Existing repositories
  may now fail, and the changelog says which rule and what to do.

## Why they are kept apart

Tooling ships often; contracts must not. If they were one number, every bug fix
would look like a change to the rules, and nobody would upgrade. Keeping them
separate means a team can take a year of tool improvements without re-auditing a
single repository.

The current release is `1.0.0` of the tooling enforcing `project/1.0` of the
contract. The two will drift apart from here, and that drift is the design.

## Changing a rule

A rule change travels as one change-set: the prose in `spec/`, the schema beside
it, the standard version, and the changelog entry. The contract and its
enforcement never ship apart.
