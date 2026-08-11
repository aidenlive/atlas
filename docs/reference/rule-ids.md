---
title: How to cite a rule
kind: reference
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2026-11-08
audience: [internal]
summary: "The identifier namespaces, what makes them stable, and how the three unnumbered standards got numbered."
---

# How to cite a rule

A rule you cannot cite is a rule you cannot waive, review, test, or argue with.

## The two kinds

| Kind | Says | Example |
|---|---|---|
| **Rule** | What must be true | `P-02` — the README opens with a hero visual |
| **Checklist item** | When you must have it | `PR-02` — Baseline: hero visual, with alt text |

One rule can be checked at several levels, and one checklist item can cover
several rules. That is why the two namespaces stay separate.

## The registry

Declared in each standard's front matter as `rule_prefixes` and
`checklist_prefixes`, and asserted by the `spec-metadata` and `rule-ids` gates.

| Standard | Rules | Checklist |
|---|---|---|
| WORKSPACE | `WK-` | — |
| PROJECT | `PJ-` | — |
| MATRIX | `MX-` | — |
| CHECKLIST | — | `ID- ST- BD- TS- CI- RL- DC- SEC- QG- OPS- CL- AX- HD- GA- GD- GX-` |
| ADMIN | `I-` invariants, `R-` roles | — |
| PRESENTATION | `P-` | `PR-` |
| LIBRARY | `L-` prompts · `L-A` all classes · `L-I` icons · `L-T` typefaces · `L-M` media | — |
| WORKSTREAM | `W-` rules, `W-I` invariants | `WS-` |
| WRITING | `WR-` | — |

## Why they are gapless

Each namespace numbers from `01` with no gaps and no repeats, and a gate
enforces it. A gap means a rule was deleted, which silently invalidates every
review comment and commit message citing it. Retiring a rule therefore means
renumbering deliberately and saying so in the changelog.

The same gate reports any bold identifier in a specification that failed to
parse as a rule, because a rule the tooling silently drops is worse than one it
rejects.

## Citing one

In review, name the rule and quote the sentence:

> The root gained a status file (`PJ-03`).

In a commit message, put it at the end:

```text
Move the status file into the tracker (PJ-03)
```

## Looking one up

```bash
atlas spec rules --grep archive
atlas spec show project --rules
```
