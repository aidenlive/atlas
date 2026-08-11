---
title: Adopt the standard in an existing repository
kind: guide
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, leadership]
summary: "Two passes: declare what is true first, fix what is wrong second."
---

# Adopt the standard in an existing repository

Nobody has time to restructure forty repositories. Nobody has to.

## The two passes

| Pass | Effort | Buys you |
|---|---|---|
| 1. Declare | An afternoon per repository | Classification, ownership, and a baseline you can measure |
| 2. Conform | Ongoing | The structure itself moves toward the standard |

Pass 1 is worth doing everywhere, immediately. Pass 2 happens repository by
repository, as each is worked on anyway.

## Pass 1: declare

1. Add `project.yaml`. Classify all eight dimensions **honestly** — an
   `experimental` project declared `stable` is worse than one declared
   `experimental`.
2. Add `admin.yaml`. Name the six duties, even if one person holds all of them.
3. Run `atlas check` and read the failures without fixing any of them yet.

At the end of pass 1 nothing is restructured, and you know what you have. That is
the point.

## Pass 2: conform

Work the gates in this order, because each makes the next cheaper:

1. `required-documents` — the missing README, LICENSE, or AGENTS.md
2. `root-closed-set` — move stray root files into a role directory
3. `no-graveyards` — delete `legacy/`; git already has it
4. `agent-guide` — one `AGENTS.md`, vendor files reduced to stubs
5. `readme-composition` — hero, description, quickstart that is true
6. Everything else

## When you cannot comply yet

Record a waiver in `project.yaml`: the item, the reason, the approver, and an
expiry. A waiver is an honest exception with a date on it. Silence is not.

```yaml
waivers:
  - item: ST-03
    reason: "Secret scanning blocked on the vendor migration; tracked in work/03."
    approver: team:platform
    expires: 2026-11-30
```

## Common objections

| Objection | Answer |
|---|---|
| "Our repositories are all different." | Their content is. Their navigation does not have to be, and that is what `P-09` buys. |
| "This is bureaucracy." | Every rule is a gate that runs in seconds. Nothing here needs a meeting. |
| "We do not have owners for all of this." | Then you found the real problem, and it was true before the standard. |

## Next

- [How the pieces fit](../architecture/repository-design.md)
- [The checklist itself](../../spec/checklist.md)
