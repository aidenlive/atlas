---
id: library
order: 7
title: LIBRARY
tagline: "The shared-asset standard: prompts, icons, typefaces, and media as versioned, validated artifacts"
question: "Where do shared assets live, and on what terms?"
version: "1.0"
status: stable
rule_prefixes: [L-, L-A, L-I, L-T, L-M, L-S]
checklist_prefixes: []
companions: [project, presentation, admin, writing]
kind: standard
owner: role:standards-maintainer
updated: 2026-08-10
review_by: 2027-02-08
audience: [internal, developers]
summary: "Shared asset classes, one home each, indexed and licensed, reviewed like code."
---

# LIBRARY: shared assets as versioned artifacts

> An asset kept in someone's downloads folder is tribal memory with a filename.
> An asset in the library is a convention with a diff.

## What this is

LIBRARY governs the reusable things: prompts carry intent, the design system
carries visual identity, icons carry marks, typefaces carry letterforms, and
media carries diagrams and reference material. It makes each a first-class,
reviewed, testable artifact rather than an attachment somebody still has.

The design system is the fleet identity `P-11` points at: one file of normative
tokens with application prose after them, consumed by everything that draws and
forked by nothing. The all-classes rules below apply to it in full — one home,
indexed, sourced, reviewed like code.

```text
library/
├── prompts/     ← reusable request prompts, one directory per category
├── design/      ← the design system: tokens and application prose (P-11)
├── skills/      ← agent skills: packaged capabilities, one directory per skill
├── icons/       ← SVG marks on a shared grid
├── typefaces/   ← families, with their licences
├── media/       ← diagrams and reference material, with their sources
└── lexicon/     ← the words this organization has standardised (WRITING)
```

## All classes

- **L-A1 One home.** An asset lives in exactly one place in `library/`. A copy
  elsewhere is a cache, and caches go stale.
- **L-A2 Indexed.** Every class carries an `index.yaml` listing every asset it
  holds. Generated from the files, so it cannot drift.
- **L-A3 Named for what it is.** `kebab-case`, describing the thing rather than
  its origin or its first use.
- **L-A4 Sourced.** Any asset derived from something else records what it was
  derived from, so it can be regenerated instead of recovered.
- **L-A5 Licensed.** Any asset the organization did not author records its
  licence and its terms. An unlicensed asset is a liability with good design.
- **L-A6 Reviewed like code.** Library changes go through pull request. There is
  no informal path into shared assets.

## Prompts

- **L-01 One objective per prompt.** A prompt that asks for three things gets one
  third of each. Two objectives are two prompts.
- **L-02 Concise.** One to three sentences. The prompt carries intent and
  constraints; the standards it invokes carry the how. Long procedure belongs in
  `docs/guides/`, referenced rather than inlined.
- **L-03 Implementation-agnostic.** Prompts name intents, standard concepts, and
  repository paths — never a specific assistant, editor, or vendor feature. The
  same file must work pasted into any assistant or handed to a person.
- **L-04 Safety is in the sentence.** Prompts for destructive or irreversible
  operations embed their guardrail: plan before acting, confirmation gates, or
  explicit refusal conditions. A prompt that can be pasted carelessly must fail
  safe.
- **L-05 Complement, do not duplicate.** Prompts cite the standards; they never
  restate their rules. When a standard changes, the prompts citing it are
  reviewed in the same change-set.
- **L-06 Location.** `library/prompts/<category>/`, plus a generated
  `index.yaml` and a human `README.md`.
- **L-07 Naming.** `request-<verb>-<object>.txt`, lowercase kebab-case. Plain
  text because prompts are paste payloads: no front matter, no markup, nothing a
  target tool could misinterpret.
- **L-08 Index integrity.** Every prompt file appears in the index, and every
  index entry resolves to a file. CI enforces both directions: an unindexed
  prompt is invisible, an indexed ghost is a lie.

### Categories

Fourteen, spanning the lifecycle. Extension follows the MATRIX policy — new
categories arrive through a versioned revision, and local ones carry an `x-`
prefix:

| | | | |
|---|---|---|---|
| `workspace` | `repository` | `architecture` | `documentation` |
| `github` | `administration` | `quality` | `security` |
| `releases` | `maintenance` | `design` | `agents` |
| `operations` | `workstreams` | | |

## Skills

A skill packages a capability an agent or a person applies as a unit: the
instructions, the assets they act on, and the metadata that names both.

- **L-S1 Self-describing.** Every skill directory carries a `skill.yaml` naming
  the skill, its version, its description, and its sources (`L-A4`). A skill
  that must be explained in chat is not yet a skill.
- **L-S2 Instructions travel with assets.** A `SKILL.md` states what the skill
  produces, what it consumes, and how to apply it. The assets it references
  live inside the skill directory, so a copied skill still works.
- **L-S3 One capability per skill.** A skill that does three things is three
  skills. Routines that compose skills reference them; they never inline them.
- **L-S4 Location and naming.** `library/skills/<skill-name>/`, kebab-case,
  named for the capability. The class index (`L-A2`) is generated from the
  `skill.yaml` files.

## Icons

- **L-I1 One concept per file, drawn on a 24px grid** with a 1.5 to 1.75px
  stroke, so a set stays visually coherent at every size.
- **L-I2 `currentColor` only.** An icon carries no baked colour, so it inherits
  its context and survives a theme change.
- **L-I3 No text inside an icon.** Text does not scale, does not translate, and
  does not survive being resized to 16px.
- **L-I4 The accessible name lives at the use site**, not in the file. The same
  icon means different things in different places.

## Typefaces

- **L-T1 The licence ships with the file.** A typeface directory contains the
  licence, or the typeface does not belong in the repository.
- **L-T2 Web formats are derived, not authored.** `woff2` is generated from the
  source, and the generation is recorded.
- **L-T3 Declare the fallback stack.** Every family records the stack that
  renders when it does not, because it sometimes will not.

## Media

- **L-M1 The source travels with the output.** A diagram records what produced
  it, so the next edit is a regeneration rather than a redraw.
- **L-M2 Prefer generated over drawn.** If a script can emit it, a script emits
  it. Generated media cannot rot without the source rotting first.
- **L-M3 Describe it in the index.** The index entry carries the description a
  person needs to choose between two similar assets without opening both.

## Usage model

**Humans** copy a prompt into any assistant, optionally appending specifics. The
prompt is the floor, not the ceiling. **Agents** may be pointed at the index to
discover sanctioned operations, with `AGENTS.md` remaining the canonical
constraints document. **Teams** treat prompt edits like specification edits. A
prompt that routinely needs local edits has a defect: fix the library, not sixty
pasted copies.

## Related

- [PROJECT](project.md) — where `library/` sits in the tree
- [PRESENTATION](presentation.md) — the fleet identity these assets carry
- [WRITING](writing.md) — the lexicon, and the prose rules prompts are held to
