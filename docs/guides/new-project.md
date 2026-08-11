---
title: Start a new project
kind: guide
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers]
summary: "Scaffold a repository that already passes, then classify it honestly."
---

# Start a new project

## Prerequisites

- The CLI installed — see [Install the CLI](install.md)
- A name in `lowercase-hyphenated`, and someone who answers for it

## 1. Scaffold

```bash
atlas init invoice-api ../invoice-api --owner team:payments
cd ../invoice-api
atlas check
```

`init` copies the starter, substitutes your facts, and runs every gate against
what it produced. Scaffolding that produces a failing repository teaches the
wrong lesson on day one.

## 2. Classify it

Open `project.yaml` and set all eight [MATRIX](../../spec/matrix.md) dimensions.
The two that people get wrong:

- **`type`** is the centre of gravity, not the technology. A service with a CLI
  is `service.api` with `interfaces: [cli]`.
- **`maturity`** is what others may lean on, not how long it has existed.
  Claiming `stable` puts the Production profile in CI (`MX-08`).

## 3. Name who answers

`admin.yaml` decomposes ownership into six duties. Assigning all six to one
principal is fine and honest; leaving them unassigned is neither.

## 4. Open the first workstream

```bash
atlas work new bootstrap-service --owner person:you
```

Write `01_plan/plan.md` before anything else.

## 5. Wire the checks in

Copy `.github/workflows/ci.yml` from the template. `atlas check` in CI is what
turns the standard from a document into a property of the repository.

## Next

- [Running the work system](work-management.md)
- [Naming and placement](../reference/conventions.md)
