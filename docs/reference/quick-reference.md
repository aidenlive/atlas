---
title: Quick reference
kind: reference
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal, developers]
summary: "The whole suite on one page: standards, namespaces, commands, and enumerations."
---

# Quick reference

## The nine standards

| # | Standard | Question | Namespaces |
|---|---|---|---|
| 1 | [WORKSPACE](../../spec/workspace.md) | Where does a file live? | `WK-` |
| 2 | [PROJECT](../../spec/project.md) | What must be true inside a repository? | `PJ-` |
| 3 | [MATRIX](../../spec/matrix.md) | What kind of project is it? | `MX-` |
| 4 | [CHECKLIST](../../spec/checklist.md) | Is it good enough? | 16 item prefixes |
| 5 | [ADMIN](../../spec/admin.md) | Who may act, who answers, who pays? | `I-` `R-` |
| 6 | [PRESENTATION](../../spec/presentation.md) | How does it show itself? | `P-` `PR-` |
| 7 | [LIBRARY](../../spec/library.md) | Where do shared assets live? | `L-` `L-A` `L-I` `L-T` `L-M` |
| 8 | [WORKSTREAM](../../spec/workstream.md) | What work is happening? | `W-` `W-I` `WS-` |
| 9 | [WRITING](../../spec/writing.md) | How is any of this written? | `WR-` |

## The rules cited most

| Rule | Short form |
|---|---|
| `WK-01` | One home per file |
| `WK-06` | Files move rightward only |
| `PJ-01` | The root is a closed set |
| `PJ-05` | The quickstart is true |
| `PJ-09` | No in-repository graveyards |
| `PJ-11` | One canonical agent guide, many pointers |
| `MX-08` | `stable` claims are checked |
| `I-4` | Elevation expires |
| `R-3` | Agents never hold `owner` |
| `P-07` | Badges are views, not facts |
| `W-10` | Progress is counted, not felt |
| `WR-05` | Claims carry evidence |

## Commands

```bash
atlas status                  # what this is, who answers, where it stands
atlas check                   # the repository against the standard
atlas lint --changed          # prose this branch touched
atlas spec show project --rules
atlas library terms           # the house vocabulary
atlas library list            # what the shared-asset library holds
atlas prompt search release
atlas work list --status blocked
atlas site build
```

## Enumerations

| Where | Values |
|---|---|
| `stage` | `idea` `incubating` `active` `maintenance` `deprecated` `archived` |
| `maturity` | `experimental` `alpha` `beta` `stable` `hardened` |
| `visibility` | `public` `internal` `restricted` `private` |
| `support` | `none` `best-effort` `business-hours` `sla` |
| Roles | `observer` `contributor` `maintainer` `admin` `owner` `steward` |
| Workstream status | `planned` `active` `blocked` `review` `done` `cancelled` |
| Task state | `todo` `doing` `blocked` `done` |
| Document status | `draft` `review` `published` `stable` `superseded` `deprecated` `retired` |

## Exit codes

`0` ok · `1` violations found · `2` bad usage · `3` not found · `4` not an Atlas
repository.
