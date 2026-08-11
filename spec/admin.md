---
id: admin
order: 5
title: ADMIN
tagline: "A universal administrative model for projects and organizations"
question: "Who may act, who answers, who pays?"
version: "1.0"
status: stable
rule_prefixes: [I-, R-]
checklist_prefixes: []
companions: [workspace, project, matrix, checklist, workstream]
kind: standard
owner: role:standards-maintainer
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, leadership]
summary: "Grants, a fixed role ladder, ownership decomposed into duties, and agents as principals that can never be accountable."
---

# ADMIN: who may act, who answers, who pays

> Structure without administration is a museum.
> Administration without structure is a bureaucracy.
> This is the fourth wall of the standard: who may do what, who answers when,
> and how anyone — human, agent, or auditor — can verify both.

## What this is

ADMIN is the model of authority for a project or an organization. It exists
because administration decays in three predictable ways: access granted broadly
and never narrowed, ownership that means nothing because it was never
decomposed, and small teams exempting themselves until they are not small.

Agents force the issue. A system that grants access by asking a person to
remember cannot survive a principal that acts a thousand times a day.

## Core concepts

| Concept | Means |
|---|---|
| **Principal** | Anything that can act: a person, a team, or an agent |
| **Grant** | A scoped, expiring permission a principal holds |
| **Role** | A named rung on the capability ladder |
| **Duty** | One decomposed component of ownership |
| **Surface** | A place authority is exercised: forge, cloud, registry, secrets |

## The role ladder

A fixed, ordered, closed set. Platforms map their native roles onto it; policy is
written against it. Every custom role is a question auditors and agents cannot
answer from the standard alone.

| Role | Capabilities (cumulative) | Typical holder |
|---|---|---|
| `observer` | Read code, docs, issues, dashboards | Stakeholders |
| `contributor` | Open issues and pull requests, comment, run CI | Anyone doing work — the default |
| `maintainer` | Merge, triage, release, edit project settings | The people who answer for the code |
| `admin` | Grant and revoke up to `maintainer`, manage integrations | Team leads, scoped to a project or team |
| `owner` | Transfer, archive, delete, change visibility | Exactly the `D6` value from `project.yaml` |
| `steward` | Org policy, billing, membership, root credentials | 2–5 named humans per org |

## Ownership, decomposed

"Owns" is a bundle, and unbundled it goes unexercised. Six duties, each held by a
named principal, defaulting to the owner but explicitly delegable:

| Duty | Answers |
|---|---|
| **Direction** | What is this for, and what is next? |
| **Code** | Who reviews and merges? |
| **Operations** | Who is paged? |
| **Security** | Who triages a disclosure? |
| **Cost** | Who owns the bill? |
| **Compliance** | Who answers an auditor? |

## The invariants

- **I-1 All authority is grants.** Nothing is implicit. If a principal can act,
  some grant says so, and the grant is discoverable.
- **I-2 Agents are principals, never people.** An agent is declared, scoped, and
  attributable to a human sponsor.
- **I-3 Grants are scoped.** A grant names its surface and its boundary. Org-wide
  by default is how the decay starts.
- **I-4 Elevation expires.** Temporary access carries an expiry at the moment it
  is granted, not a promise to revisit.
- **I-5 Two keys for irreversible acts.** Deleting, transferring, changing
  visibility, or rotating root credentials requires two named principals.

## Rules of the ladder

- **R-1 Default to `contributor` at the narrowest useful scope.**
  Broad-by-default is where decay begins.
- **R-2 One source of truth for ownership.** `owner` here and `D6` in
  `project.yaml` are the same fact; the manifest points at this document.
- **R-3 Agents may hold at most `maintainer`, with an expiry.** Never `owner`,
  never `steward`. An agent can do a maintainer's work; it cannot answer for an
  organization.
- **R-4 Steward count is bounded.** At least two for bus factor, at most five for
  accountability. A twelve-steward org has no stewards.

## Surfaces and drift

Authority is exercised on more than the forge: cloud accounts, package
registries, secret stores, and dashboards each carry grants. Each surface names
the principal accountable for it, and each is reviewed on a declared cadence.

Drift is the expected state, so it is measured rather than assumed away: an
access review compares granted authority against declared authority and reports
the difference. A review that never finds drift is not a review.

## Conformance profiles

| Profile | For | Requires |
|---|---|---|
| **Solo** | One person, no org | Owner declared; `I-4`, `I-5` on irreversible acts |
| **Team** | A team with shared surfaces | Full ladder, duties assigned, quarterly access review |
| **Org** | Multiple teams, billing, compliance | Stewards bounded, surfaces enumerated, audit trail retained |

Small is not exempt. The solo profile is smaller, not weaker: a single person is
exactly the case where an expired grant is never noticed.

## Related

- [MATRIX](matrix.md) — where ownership is declared
- [WORKSTREAM](workstream.md) — how authority flows into day-to-day work
- [CHECKLIST](checklist.md) — the gates that verify ownership resolves
