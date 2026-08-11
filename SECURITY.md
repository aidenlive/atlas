# Security policy

## Scope

Atlas is a set of standards and a command-line tool. It reads files and writes
only where you tell it to. It makes no network requests, runs no code from the
repositories it checks, and holds no credentials.

The realistic risks are small but not zero:

- A crafted manifest or Markdown file causing the tool to read outside the
  repository, or to hang.
- A dependency vulnerability in `PyYAML` or `jsonschema`.
- A generated artifact whose content comes from a manifest and is rendered
  somewhere that trusts it.

## Supported versions

The most recent minor release of `atlas-standard` receives fixes.

## Reporting

Report privately to `security@example.com`. Include the version, the input that
triggers it, and what you observed. Do not open a public issue for an unfixed
vulnerability.

| When | What |
|---|---|
| Within 3 working days | Acknowledgement that a person has it |
| Within 10 working days | An assessment, and a fix or a plan with a date |
| On release | A changelog entry, and credit if you want it |

## Out of scope

The content of repositories that use Atlas. If something should not have been
published, that is a governance failure, not a tooling vulnerability — ADMIN
says who answers for it.
