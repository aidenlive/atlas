---
id: writing
order: 9
title: WRITING
tagline: "The prose standard: how everything in this suite is written"
question: "How is any of this written?"
version: "1.0"
status: stable
rule_prefixes: [WR-]
checklist_prefixes: []
companions: [project, presentation, library, checklist]
kind: standard
owner: role:editorial-lead
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, developers, public]
summary: "One voice, one spelling per name, and the composition rules that make a README, an ADR, and a runbook read like one organization."
---

# WRITING: how any of this is written

> Every other standard in this suite governs the shape of the work.
> This one governs the sentences, because a repository is mostly prose and
> nobody had written down what good looked like.

## What this is

WRITING is the newest standard and the smallest in scope. It does not govern
what a repository contains — [PROJECT](project.md) does that — nor how it
displays itself — [PRESENTATION](presentation.md) does that. It governs the
words inside: READMEs, specifications, ADRs, guides, runbooks, changelogs,
commit messages, and prompts.

It exists for two reasons. "Make it clearer" is the least actionable review
comment available. And a fleet that presents one shape (`P-09`) but sounds like
eleven different people has solved half the problem.

The mechanical half of this standard is checked by `atlas lint`. The rest is a
reviewer's judgement, deliberately.

## The voice

We sound like **a capable colleague explaining something they know well**. Not a
brand, not a spokesperson, not a manual.

| We are | We are not | Because |
|---|---|---|
| Clear | Simplistic | The reader is capable; the subject may be hard |
| Direct | Blunt | Say the thing. Saying it kindly costs nothing |
| Concrete | Vague | A number, a name, or an example beats an adjective |
| Human | Chummy | Written by a person, not performing friendliness |

Tone moves along one axis — how much room the reader needs. Grammar,
terminology, and structure do not relax because a channel is casual.

## The rules

### Voice

- **WR-01 One voice across the fleet.** A reader who cannot tell which team wrote
  something is the goal, not a side effect.
- **WR-02 Second person, active verbs.** `You can revoke a key`, or
  `The service revokes the key`. Passive voice only where the actor is genuinely
  unknown.
- **WR-03 The shorter word.** Where two words mean the same thing, use the
  shorter. The lexicon lists the ones already decided.
- **WR-04 One sentence, one idea.** A sentence past 34 words is usually two
  sentences wearing one coat.
- **WR-05 Claims carry evidence.** No superlative without a number, a source, or
  a named example. `Fastest available` is a claim; `2.1× faster on the same
  fleet` is a sentence.
- **WR-06 Say the hard thing first.** Breaking changes, limitations, and bad news
  go in the first paragraph. Burying them only moves the reader's anger to the
  moment they find out.

### Language

- **WR-07 One spelling per name.** Every product, tool, role, and system has one
  written form, recorded in `library/lexicon/terms.yaml`. Alternatives are listed
  so they fail a check rather than an argument.
- **WR-08 Every avoidance names its replacement.** A lexicon entry that forbids a
  phrase says what to write instead. A rule without a remedy is a complaint.
- **WR-09 Sentence case, serial commas, ISO dates in data.** Headings and labels
  in sentence case; `red, white, and blue`; `2026-08-08` in manifests and tables,
  `8 August 2026` in a sentence.
- **WR-10 Expand on first use.** Spell an acronym out the first time, then use
  it. Inclusive, plain terms throughout: `allowlist`, `main`, `primary`.

### Composition

- **WR-11 Lead with the answer.** The first screen says what this is and what to
  do. Background comes after. This is `P-06` applied to every document, not only
  the README.
- **WR-12 One title, headings that descend one at a time.** One H1 matching the
  declared title; no jumping levels; nothing deeper than H4. If you need H5, the
  document is two documents.
- **WR-13 Structure earns its place.** A table when attributes are compared, a
  numbered list when order matters, a callout when something must not be missed.
  Formatting with no informational job is noise.
- **WR-14 Link text names its destination.** Never `click here`, and every
  relative link resolves.
- **WR-15 One fact, one home.** State a fact once and link to it. Every duplicate
  is a future contradiction — the prose form of `WK-01`.
- **WR-16 Every document declares itself.** Front matter carrying `title`,
  `kind`, `owner`, `status`, and `updated`, so ownership survives a
  reorganisation and staleness is visible.

## Before and after

> **Before**
> In order to facilitate a seamless onboarding experience, it is important to
> note that new users may be required to potentially verify their identity prior
> to accessing certain functionality within the platform.

> **After**
> New users verify their identity before they can invite teammates or move money.
> Everything else works immediately.

Twenty-two words instead of thirty-four, both gated actions named, and the
reader's actual question answered. Rules applied: `WR-03`, `WR-04`, `WR-05`.

## What is checked, and what is not

| Checked by `atlas lint` | Left to a reviewer |
|---|---|
| Front matter, headings, link text, terminology, phrasing, sentence length | Whether the argument holds |
| Trailing whitespace, tabs, emphasis density | Whether the example is the right example |
| That every relative link resolves | Whether the reader will care |

A warning is a judgement call. A 40-word sentence may be the right sentence, and
a writer is allowed to keep it.

## Related

- [PRESENTATION](presentation.md) — the shape the prose sits inside
- [LIBRARY](library.md) — where the lexicon and the prompts live
- [CHECKLIST](checklist.md) — `DC-05`, the gate that requires this
