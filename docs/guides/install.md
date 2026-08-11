---
title: Install the CLI
kind: guide
owner: role:standards-maintainer
status: published
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers]
summary: "Install the atlas command, or run it from a checkout with no install at all."
---

# Install the CLI

You do not need the CLI to follow the standards — they are prose in `spec/`. You
need it to have them checked for you.

## Prerequisites

- Python 3.10 or newer
- Git, for `atlas lint --changed`

## Install

```bash
pip install atlas-standard
atlas --version
```

Two runtime dependencies, both load-bearing: one parses the manifests, one
validates them. Everything else is standard library, so the tool starts fast
enough to live in a pre-commit hook.

## Run it from a checkout instead

```bash
git clone https://github.com/OWNER/atlas
cd atlas
scripts/atlas check
python -m pytest tests/ -q
```

## Check the install

```bash
atlas doctor
```

`doctor` reports on the environment and the repository, and names the remedy for
anything it finds. A diagnosis without a next step is bad news, not help.

## Next

- [Start a new project](new-project.md)
- [Adopt the standard where a repository already exists](adoption.md)
- [CLI reference](../reference/cli.md)
