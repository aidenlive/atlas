---
id: checklist
order: 4
title: CHECKLIST
tagline: "The minimum bar. Quality gates for every project, from first commit to production"
question: "Is it good enough?"
version: "1.0"
status: stable
rule_prefixes: []
checklist_prefixes: [ID-, ST-, BD-, TS-, CI-, RL-, DC-, SEC-, QG-, OPS-, CL-, AX-, HD-, GA-, GD-, GX-]
companions: [project, matrix, presentation, workstream]
kind: standard
owner: role:standards-maintainer
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers, leadership]
summary: "Four accumulating profiles keyed to Matrix maturity, plus the three stage gates."
---

# CHECKLIST: is it good enough?

> A checklist is a promise made checkable.
> "Production-ready" is not a feeling; it is this document returning green.

## How to use this

**Profiles, not one bar.** Requirements accumulate across four profiles keyed to
[MATRIX](matrix.md) `D3` maturity. A project claims a level by passing that
profile, and `MX-08` makes the claim CI-enforced.

| Profile | Claimed maturity | Means |
|---|---|---|
| **Baseline** | any repository | It can be found, run, and understood |
| **Beta** | `beta` | Other people can rely on it a little |
| **Production** | `stable` | Other people can depend on it |
| **Hardened** | `hardened` | It carries critical paths |

**Two marks.** `☐` is mechanically checkable and belongs in CI. `🧭` needs human
judgement and belongs in review.

**Conditional items** carry their condition in brackets, e.g. `[vis: public]`.
An item whose condition does not apply is not a waiver; it is out of scope.

## Baseline — every repository

### Identity and documents

- ☐ **ID-01** `README.md` present and following the `PJ-04` skeleton
- ☐ **ID-02** `project.yaml` present, schema-valid, all eight dimensions classified
- ☐ **ID-03** `LICENSE` present `[vis: public]`, or visibility declared internal or private
- ☐ **ID-04** `AGENTS.md` present with all seven sections
- ☐ **ID-05** Vendor agent files are stubs of three lines or fewer pointing at `AGENTS.md`
- ☐ **ID-06** `CHANGELOG.md` present, Keep a Changelog format, `Unreleased` section exists
- 🧭 **ID-07** The quickstart is actually true: a stranger on a clean machine reaches first success by copy-paste alone

### Structure and hygiene

- ☐ **ST-01** Root is the `PJ-01` closed set: no stray files, no graveyard directories
- ☐ **ST-02** `.gitignore` covers build output, dependency directories, and environment files
- ☐ **ST-03** No secrets in tree or history; secret scanning enabled and verified clean
- ☐ **ST-04** All shipped code under one source root; tests mirror it
- ☐ **ST-05** Default branch protected `[ownership: team|community]`; force-push disabled

### Build and run

- ☐ **BD-01** One documented command installs dependencies; one builds; one runs
- ☐ **BD-02** Dependencies pinned or locked, and the lockfile is committed
- ☐ **BD-03** Build is reproducible on a clean machine, verified in CI
- ☐ **BD-04** Runtime prerequisites stated with versions

## Beta — claiming `maturity: beta`

### Testing

- ☐ **TS-01** Automated test suite covering the quickstart path and documented behaviour
- ☐ **TS-02** Tests run in CI on every pull request
- ☐ **TS-03** Coverage measured and reported; regressions visible
- ☐ **TS-04** Tests are deterministic; flaky tests quarantined with an owner and a date
- 🧭 **TS-05** Failure output tells a stranger what broke and where

### Continuous integration

- ☐ **CI-01** CI runs on every pull request and blocks merge on failure
- ☐ **CI-02** Lint, format, and type checks run in CI, not advisorily
- ☐ **CI-03** CI runs on the supported platform and version matrix
- ☐ **CI-04** Build artifacts produced by CI, not by a laptop
- ☐ **CI-05** CI configuration lives in the repository as code

### Releases and versioning

- ☐ **RL-01** Versioning scheme declared: SemVer, or CalVer for continuously deployed apps
- ☐ **RL-02** Releases tagged `vX.Y.Z` and derived from the changelog
- ☐ **RL-03** Release process is one documented command or workflow
- ☐ **RL-04** Published artifacts match a tagged commit

## Production — claiming `maturity: stable`

### Documentation

- ☐ **DC-01** `docs/` carries architecture, decisions, guides, and reference
- ☐ **DC-02** Reference documentation generated from source where the ecosystem allows
- ☐ **DC-03** Every documented example runs in CI
- ☐ **DC-04** Architecture decisions recorded as dated ADRs
- 🧭 **DC-05** Prose passes [WRITING](writing.md); `atlas lint` reports no errors

### Security

- ☐ **SEC-01** Dependency vulnerability scanning in CI; no unwaived critical findings
- ☐ **SEC-02** Automated dependency updates enabled and not rotting
- ☐ **SEC-03** `SECURITY.md` with a disclosure channel `[vis: public]`
- ☐ **SEC-04** Static analysis appropriate to the stack running in CI
- ☐ **SEC-05** Least-privilege CI: scoped tokens, no long-lived credentials
- 🧭 **SEC-06** One-page threat model in `docs/architecture/` `[type: service.*, app.*]`

### Quality gates

- ☐ **QG-01** Linter and formatter enforced, ending style debate by tooling
- ☐ **QG-02** Type checking enforced where the ecosystem supports it
- ☐ **QG-03** Review required for every change; `CODEOWNERS` routes it; no self-merge
- ☐ **QG-04** Breaking changes gated: semver-major, migration notes, deprecation window

### Operations `[deploy: ≠ none]`

- ☐ **OPS-01** Deployment is automated and repeatable from a tagged commit
- ☐ **OPS-02** Rollback procedure documented and exercised
- ☐ **OPS-03** Health checks and structured logging in place
- ☐ **OPS-04** Runbook in `docs/guides/` covering the top three failure modes
- ☐ **OPS-05** Configuration and secrets injected, never committed

### Compliance and legal

- ☐ **CL-01** Dependency licences inventoried and compatible with `LICENSE`
- ☐ **CL-02** Third-party assets carry their source and licence
- ☐ **CL-03** Data handling documented `[handles personal data]`

### Accessibility and experience `[type: app.*]`

- ☐ **AX-01** Keyboard navigable; visible focus states
- ☐ **AX-02** Colour is never the only signal; contrast meets WCAG AA
- 🧭 **AX-03** Screen-reader pass on the primary flow

## Hardened — claiming `maturity: hardened`

- ☐ **HD-01** Security review completed and dated, findings tracked to closure
- ☐ **HD-02** Service level objectives declared and measured
- ☐ **HD-03** On-call rotation named, with escalation in `authority` terms
- ☐ **HD-04** Disaster recovery tested, with a recorded date and result
- ☐ **HD-05** Supply chain: artifacts signed, provenance attested

## Stage gates

### Gate `incubating → active`

- ☐ **GA-01** Baseline profile passes in full
- ☐ **GA-02** Owner declared and resolvable in [ADMIN](admin.md)
- ☐ **GA-03** Quickstart verified by someone who did not write it

### Gate `active | maintenance → deprecated`

- ☐ **GD-01** Successor named, or explicitly "none"
- ☐ **GD-02** Sunset date set and published in the README
- ☐ **GD-03** Consumers notified through the channel they actually read

### Gate `deprecated → archived`

- ☐ **GX-01** Repository archived on the forge, making the state mechanically true
- ☐ **GX-02** Final changelog entry recording the ending and the successor
- ☐ **GX-03** Ownership transferred or formally released; no `unowned` past 90 days

## Waivers

An item may be waived by recording the item id, the reason, the approver, and an
expiry in the manifest. A waiver without an expiry is a silent exception, and a
waiver renewed more than twice is a decision to change the item or the claim.

## Related

- [MATRIX](matrix.md) — the maturity levels these profiles key off
- [PROJECT](project.md) — the structural rules these items check
- [WRITING](writing.md) — the prose bar behind `DC-05`
