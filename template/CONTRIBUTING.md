# Contributing

## Before you open a pull request

```bash
atlas check
atlas lint --changed
```

## How change happens here

Branch, pull request, green CI, review, merge (PJ-15). Direct pushes to the
default branch are disabled by branch protection: the rule is mechanical, not
cultural.

## Conventions

- Branches: `type/short-description`
- Commits: Conventional Commits — `feat:`, `fix:`, `docs:`, `chore:`
- Documents: `kebab-case.md`; decisions as `NNNN-short-title.md`
- Anything a linter can enforce, a linter enforces (PJ-16)

## Decisions

A choice that outlives its pull request becomes an ADR in `docs/decisions/`.
Accepted ADRs are immutable: supersede one, never edit it (PJ-08).
