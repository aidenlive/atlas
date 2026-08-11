# Contributing

Two kinds of change, held to different bars.

| Change | Needs |
|---|---|
| Editorial, tooling, or a prompt | One reviewer |
| A rule added, changed, or removed | The standards maintainer and the owner |

## Before you open a pull request

```bash
scripts/atlas check
scripts/atlas lint --changed --strict
python -m pytest tests/ -q
```

## Changing a rule

A rule change travels as one change-set:

1. The prose in `spec/`.
2. The schema beside it, if the change is machine-checkable.
3. The standard version in `project.yaml`, if the contract moved — see
   [versioning](docs/reference/versioning.md).
4. A `CHANGELOG.md` entry naming the rule and what to do about it.

Rule identifiers are permanent addresses. Removing one means renumbering
deliberately and saying so, because review comments and commit messages already
cite it.

## Adding a gate

Register it in `src/atlas/core/compliance.py` with an id, a summary, and **the
rule it enforces**. A gate that cannot cite a rule is a preference.

## Adding a prompt

One objective, three sentences at most, plain text, `request-<verb>-<object>.txt`.
Destructive operations carry their guardrail in the sentence (`L-04`). Then:

```bash
python scripts/build_library.py
```

## Changing the design system

`library/design/DESIGN.md` is the one source of visual identity (`P-11`). After
editing it:

```bash
python scripts/build_design.py
python scripts/build_assets.py
python scripts/build_screenshots.py
```

The `design-current` gate fails when a derivation is stale.

## Generated files

Never edit these by hand; the next run overwrites them and a gate will notice:

- `docs/reference/cli.md`
- `library/prompts/index.yaml`
- `library/design/index.yaml`, `assets/design/tokens.yaml`
- `work/README.md`, `work/index.yaml`
- `assets/badges/*.svg`, `assets/demo-*.svg`

## Commit messages

Conventional Commits, with any rule identifiers at the end:

```text
fix: move the status file into the tracker (PJ-03)
```
