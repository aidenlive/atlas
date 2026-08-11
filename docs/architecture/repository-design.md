---
title: How the pieces fit
kind: explainer
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-08-08
audience: [internal, developers]
summary: "Why the standards, the schemas, the library, and the tooling are shaped the way they are."
---

# How the pieces fit

## The shape

```text
spec/          the product: nine standards + JSON Schemas
src/atlas/     the tooling: core library, then a CLI on top of it
library/       shared assets: prompts, the design system, the lexicon
work/          every initiative as a numbered workstream + generated dashboard
template/      a starter repository that passes what it teaches
docs/          guides, reference, architecture, decisions
examples/      worked manifests, validated in CI
tests/         self-hosting, schema, parser, linter, CLI, and template checks
scripts/       thin wrappers and generators
assets/        badges and terminal demos, generated from real output
```

## Prose and schema, kept in step

The prose in `spec/` is the standard. The JSON Schemas beside it encode the part
a machine can check. Both describe the same contract, so a value added to one
must be added to the other. Tests compare them, because two sources of truth
that nobody compares are only two sources.

## Declared, then checked

Every repository states its own facts: `project.yaml` for what it is,
`admin.yaml` for who may act, front matter for each document. Nothing is
inferred from directory names or file counts. Declaration makes the facts
reviewable in a diff; checking makes them true.

## Library first, CLI second

Everything the CLI does can be imported from `atlas.core` with no terminal
involved. One body of code therefore serves the command line, the test suite,
CI, and anything built on top. The CLI is a presentation layer over a library,
rather than a program with functions hidden inside it.

## Generated views cannot outrun their source

| Artifact | Generated from |
|---|---|
| `docs/reference/cli.md` | The argument parser |
| `library/prompts/index.yaml` | The prompt files |
| `work/README.md`, `work/index.yaml` | The task tables |
| `assets/design/tokens.yaml` | `library/design/DESIGN.md`, the design system |
| `assets/badges/*.svg` | `project.yaml` and the design tokens |
| `assets/demo-*.svg` | Running the commands and capturing the output |

A badge cannot claim something the manifest no longer says. A dashboard cannot
report progress the task table does not show. A screenshot cannot show a result
the tool does not produce.

## The two checkers

`atlas check` asks whether the **repository** is in order: 24 gates over
manifests, structure, documents, the library, work, and prose. `atlas lint` asks
whether a **document** is: 11 rules from WRITING.

They are separate because they answer different questions at different moments.
CI runs both; a writer mid-draft runs only the second.

## Related

- [Why the CLI is shaped this way](cli-design.md)
- [The decision records](../decisions/0001-gates-as-a-registry.md)
