---
title: Waivers, not exemptions
kind: decision
owner: team:standards
status: published
updated: 2026-08-08
audience: [internal, leadership]
summary: "Why exceptions live in the manifest with an expiry rather than in the tool's exclusion list."
---

# 2. Waivers, not exemptions

Date: 2026-08-08

## Status

Accepted.

## Context

Every standard meets a case it cannot yet accommodate. There are two ways to
handle it. Exempt the case in the tooling — an exclusion list, a special case, a
skipped gate — or record it as a dated exception in the repository's own
manifest.

The first is invisible. Six months later nobody knows the exemption exists,
which rule it suspends, or whether the reason still holds. An exception nobody
can see is an exception nobody can retire.

## Decision

Exceptions are **waivers** in `project.yaml`, naming four things:

```yaml
waivers:
  - item: ST-01
    reason: "…"
    approver: team:standards
    expires: 2027-02-08
```

The gate the item belongs to reads waivers and honours an unexpired one. The
`waivers-honest` gate fails on any waiver with no expiry, or a lapsed one.

## Consequences

Every exception is greppable, reviewable in a diff, attributable to an approver,
and self-removing. A waiver renewed more than twice is a decision to change the
item or the claim, which is a conversation the expiry forces someone to have.

The tooling keeps one exclusion list, `EXCLUDED_DIRS`, and it governs only where
the tool *walks* — not what the standard permits.
