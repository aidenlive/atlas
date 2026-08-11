---
title: Running the work system
kind: guide
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal]
summary: "One numbered directory per initiative, nine sections, and progress counted from the task table."
---

# Running the work system

Work goes wrong in a predictable way: the plan is in someone's head, the status
is in a chat thread, and the evidence is in an attachment. `work/` puts all three
in the repository.

## Opening one

```bash
atlas work new migrate-the-fleet --owner person:you
```

That creates a numbered directory with nine sections. Write `01_plan/plan.md`
before anything else: objective, scope, milestones.

## Tracking

Status lives in one table, `02_tasks/tasks.md`. Four states and no others
(`W-13`): `todo`, `doing`, `blocked`, `done`.

```bash
atlas work list --status blocked
atlas work show 01 --tasks
```

## Regenerating the views

```bash
atlas work sync
```

This rewrites `work/README.md`, the dashboard a person reads, and
`work/index.yaml`, the file an agent reads. Both are generated from the task
tables, so progress is counted rather than claimed (`W-10`).

> **Warning**
> Never hand-edit either file. The `generated-current` gate will notice, and the
> next sync overwrites the edit.

## Finishing

A workstream reaches `done` when `07_validation/criteria.md` carries evidence,
not when it feels finished (`W-I5`). Then it stays where it is: a closed
workstream is the record of why the work says what it says (`W-04`).

## Working with agents

Assignments, constraints, and expiry live in `08_agents/agents.md`. An agent
holds exactly the authority [ADMIN](../../spec/admin.md) grants it, and never
`owner` (`R-3`). A handoff is a written artifact, not a conversation (`W-16`).

## Next

- [WORKSTREAM](../../spec/workstream.md), the standard behind all of this
- [ADMIN](../../spec/admin.md), for who may act
