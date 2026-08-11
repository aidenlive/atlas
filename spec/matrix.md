---
id: matrix
order: 3
title: MATRIX
tagline: "The canonical taxonomy of software projects"
question: "What kind of project is it?"
version: "1.0"
status: stable
rule_prefixes: [MX-]
checklist_prefixes: []
companions: [project, checklist, admin]
kind: standard
owner: role:standards-maintainer
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers, leadership]
summary: "Eight independent dimensions, closed enumerations, and the cross-dimension grammar that keeps a manifest honest."
---

# MATRIX: the canonical taxonomy of projects

> You cannot govern what you cannot classify.
> The Matrix gives every project a coordinate, and gives every tool, agent, and
> policy a handle to grab.

## What this is

MATRIX defines the controlled vocabulary used by `project.yaml`. Every project is
classified along **eight independent dimensions**, addressed `D1` through `D8`.
Values are closed enumerations: tools validate against them, checklists key off
them, and dashboards aggregate over them.

The dimensions are independent on purpose. A young project can be solid; an old
one can be fragile. Conflating "how far along" with "how much you may lean on it"
produces the two classic lies — *1.0 therefore reliable*, and *0.x therefore
excused*.

## D1 · Type — what it is

Six families, split by **who the consumer is**, because consumer identity (not
technology) decides what CHECKLIST demands.

| Family | Values | Consumer holds |
|---|---|---|
| `app` | `web` `mobile` `desktop` `tui` | A URL, a store listing, an installer, a session |
| `lib` | `package` `framework` `sdk` `plugin` | A version constraint, or a host system |
| `service` | `api` `worker` `gateway` `mcp` | An endpoint and a contract, or a tool list |
| `tool` | `cli` `action` `script` | A command, or a pipeline step |
| `platform` | `infra` `design` `template` `config` | Infrastructure, UIs, other projects, tools |
| `content` | `docs` `spec` `data` `research` | Prose, citations, a download, findings |

Hybrids declare a primary type by centre of gravity, plus
`interfaces: [http-api, cli, sdk, ui, mcp]` enumerating the other surfaces.

## D2 · Stage — where it is in life

```yaml
stage: [idea, incubating, active, maintenance, deprecated, archived]
transitions:
  idea:        [incubating, archived]
  incubating:  [active, archived]
  active:      [maintenance, deprecated]
  maintenance: [active, deprecated]     # re-activation is a declared event
  deprecated:  [archived]
  archived:    []                       # terminal; revival is a new project
constraints:
  deprecated: { requires: [successor, sunset_date] }
  archived:   { requires: [forge_archived: true] }
```

## D3 · Maturity — how trustworthy it is

| Level | Value | Meaning | Objective bar |
|---|---|---|---|
| 0 | `experimental` | May not work; may vanish | Builds |
| 1 | `alpha` | Works for its author | Builds, smoke tests, quickstart true |
| 2 | `beta` | Works for early adopters | Test suite, CI, versioned releases |
| 3 | `stable` | Works as documented | CHECKLIST Production profile passes |
| 4 | `hardened` | Trusted for critical paths | Stable, plus security review, SLOs, runbook |

## D4–D8 · The remaining dimensions

| Dimension | Values |
|---|---|
| `D4` **Packaging** — how it ships | `registry` `container` `binary` `installer` `bundle` `source` `none` |
| `D5` **Deployment** — how it runs | `none` `client` `serverless` `managed.paas` `managed.k8s` `selfhosted` `embedded` |
| `D6` **Ownership** — who answers | `team:<name>` `person:<handle>` `community` `unowned` |
| `D7` **Visibility** — who may see it | `public` `internal` `restricted` `private` |
| `D8` **Support** — what users may expect | `none` `best-effort` `business-hours` `sla` |

## The rules

- **MX-01 Eight dimensions, always.** A manifest classifies all eight. A
  dimension left blank is a question someone will answer wrongly later.
- **MX-02 Values are closed enumerations.** A value outside the enum fails
  validation. New values arrive through a standard revision, not a local edit.
- **MX-03 Classify by centre of gravity.** A hybrid picks one primary type and
  enumerates its other surfaces under `interfaces`.
- **MX-04 Stages move rightward only.** Re-activation from `maintenance` is the
  single leftward move, and it is a declared event with a changelog entry.
- **MX-05 `deprecated` requires a successor and a sunset date.** Naming "none" as
  the successor is allowed; leaving it unanswered is not.
- **MX-06 `archived` must be mechanically true.** The repository is archived on
  the forge, not merely labelled.
- **MX-07 Stage and maturity are independent.** Neither implies the other, and a
  maturity downgrade is a changelog event with a README banner. Silent downgrades
  are banned.
- **MX-08 `stable` claims are checked.** Claiming `maturity: stable` puts the
  CHECKLIST Production profile in CI. An unchecked claim is marketing.
- **MX-09 `unowned` is a defect, not a category.** It is legal only during a
  `deprecated` to `archived` transition, for at most 90 days.
- **MX-10 Ownership resolves to a principal.** The `D6` value and the `owner`
  role in [ADMIN](admin.md) are the same fact, recorded once.

## Worked examples

```yaml
# a published CLI, trusted, self-contained
type: tool.cli        stage: active       maturity: stable
packaging: binary     deploy: none        ownership: team:platform
visibility: public    support: best-effort

# an internal API on the way out
type: service.api     stage: deprecated   maturity: stable
packaging: container  deploy: managed.k8s ownership: team:payments
visibility: internal  support: business-hours
successor: billing-api   sunset_date: 2026-12-31
```

## Related

- [PROJECT](project.md) — where the manifest lives and what surrounds it
- [CHECKLIST](checklist.md) — the bar each maturity level must pass
- [ADMIN](admin.md) — who the ownership value points at
