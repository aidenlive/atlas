---
id: workspace
order: 1
title: WORKSPACE
tagline: "An open standard for organizing digital work"
question: "Where does a file live?"
version: "1.0"
status: stable
rule_prefixes: [WK-]
checklist_prefixes: []
companions: [project, writing]
kind: standard
owner: role:standards-maintainer
updated: 2026-08-08
review_by: 2027-02-08
audience: [internal, public]
summary: "One home per file, lifecycle at the top, and names that survive being pasted into a chat message."
---

# WORKSPACE: an open standard for organizing digital work

> A filesystem is not storage. It is the operating system of your attention.
> Organize it once, correctly, and never think about it again.

## What this is

WORKSPACE governs the filesystem *around* your work: the tree on every machine
you use, before any repository exists. [PROJECT](project.md) governs what must
be true *inside* a repository. The two meet at `code/`.

Every computer eventually becomes disorganized for the same four reasons, and
each rule below answers one of them:

| Failure | Why it happens | Answered by |
|---|---|---|
| Filing debt | Filing costs a decision at the worst moment | `WK-03` |
| Topic drift | "Aboutness" is ambiguous; doing-state is not | `WK-02` |
| Deep hierarchies | Every level is a tax at filing *and* at retrieval | `WK-04` |
| Archive distrust | Garbage was archived instead of deleted | `WK-14` |

Search is not a substitute. Search finds what you can name; structure answers
what you cannot — what is unfinished, what is shared, what is done.

## The lifecycle

Every file moves through at most five stages, and the directory it sits in *is*
its stage. No metadata required.

```text
CAPTURE ──▶ ACTIVE ──▶ REFERENCE ──▶ ARCHIVE ──▶ (DISPOSE)
 00_inbox    01–04       within        05_archive   trash
             spaces      spaces
```

| Stage | Lives in | Residence |
|---|---|---|
| Capture | `00_inbox` | Days. It has no decision attached yet |
| Active | `01_personal` … `04_shared` | The life of the task |
| Reference | `reference/` inside its space | Stable but consulted |
| Archive | `05_archive/YYYY/` | Forever, immutable |
| Dispose | Trash | Never archived. Archiving garbage is how archives lose trust |

## The canonical hierarchy

```text
~/                          (or the workspace root)
├── README.md               ← sentinel: explains the structure in place
├── 00_inbox/               ← capture. drained on a schedule, never stores.
├── 01_personal/            ← private life. personal cloud only.
├── 02_work/                ← current employer. leave job, archive the folder.
├── 03_projects/            ← self-directed work with a definition of done.
│   ├── active/  paused/  ideas/
├── 04_shared/              ← jointly owned with specific people.
├── 05_archive/YYYY/        ← finished. immutable. organized by time.
├── code/                   ← repositories (own lifecycle: git)
│   ├── work/  personal/  playground/  forks/
├── notes/                  ← one flat notes vault (own lifecycle: links)
├── assets/                 ← reusable raw material: fonts, icons, media
└── scripts/                ← the automation that runs this workspace
```

Why these choices, briefly:

- **Numeric prefixes are the API.** They force lifecycle order in every file
  browser on every operating system, and give scripts a stable anchor to grep.
- **`00_inbox` exists so nowhere else has to tolerate mess.** It is the only
  folder allowed to be chaotic, which is what keeps the other five clean.
- **`01_personal` against `02_work` is a sync and trust boundary**, not a topic
  boundary: different clouds, different backups, and on the day you change jobs,
  different fates.
- **`code/`, `notes/`, `assets/`, `scripts/` sit outside the numbered spaces**
  because each already has a stronger native lifecycle — git history, links,
  reuse, execution — that capture-to-archive would fight rather than help.

## The rules

- **WK-01 One home per file.** Every file has exactly one canonical location.
  Copies are caches, links are pointers, the home is truth. Duplication is where
  "which one is real?" is born.
- **WK-02 Lifecycle over topic at the top.** The root encodes what you are
  *doing* with information, never what it is *about*.
- **WK-03 Capture is free, filing is scheduled.** Nothing may demand a filing
  decision at arrival time. Everything lands in `00_inbox`; filing happens in
  batches, on a schedule.
- **WK-04 Shallow beats deep.** Three levels below the root is the working
  maximum.
- **WK-05 Time is the only safe global taxonomy.** When in doubt, organize by
  year. Dates never get renamed, merged, or reconsidered.
- **WK-06 Files move rightward only.** A revived project is a *new* folder in
  `03_projects` that may copy from the archive. The archived original never
  moves back. This one rule is what makes the archive trustworthy.
- **WK-07 The hierarchy is a closed set.** The six numbered spaces and the four
  outboard directories are the whole top level. A new need goes inside an
  existing space or triggers a deliberate revision, never an ad-hoc root entry.
- **WK-08 Dates lead, and dates are ISO.** `2026-08-03_invoice_acme.pdf`.
  ISO 8601 sorts chronologically as a side effect of sorting alphabetically.
- **WK-09 One case convention, ASCII only.** `lowercase_with_underscores` or
  hyphens — pick one per workspace and never revisit it. Characters limited to
  `a-z 0-9 _ - .`, the intersection of every filesystem, shell, and URL encoder
  you will meet.
- **WK-10 Names survive amnesia.** The test: would the name make sense pasted
  alone into a chat message, stripped of its folder? `report.pdf` fails;
  `2026-06_q2-board-report_finmetrics.pdf` passes. Folders give context at home,
  names give context in transit.
- **WK-11 Versions are explicit and terminal.** Use `_v1`, `_v2` while drafting.
  `final_v2_REAL` is the punchline of a failed system: when a document is done it
  stops versioning by moving to the archive.
- **WK-12 A sentinel README explains the structure in place.** A standard nobody
  can discover where they landed is folklore.
- **WK-13 Sync policy is declared per space.** `00_inbox` is local only,
  `01_personal` is personal cloud, `02_work` is the employer's platform,
  `05_archive` is replicated but never live-synced. Live sync on immutable data
  is pure risk.
- **WK-14 Dispose instead of archiving garbage.** The archive holds records, not
  everything that survived. One deletion pass at archive time is what keeps the
  archive worth searching.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| `Desktop/` as a workspace | Capture surface pretending to be storage; violates `WK-01`, `WK-03` |
| `misc/`, `stuff/`, `temp/` outside the inbox | Names that describe no lifecycle stage; violates `WK-02` |
| Deep topic trees (`work/clients/acme/2025/q3/...`) | Filing tax and retrieval guesswork; violates `WK-04` |
| Dated copies of the same file | Versioning where archiving belongs; violates `WK-11` |
| A living archive | Mutation destroys the guarantee; violates `WK-06` |

## Related

- [PROJECT](project.md) — what must be true inside a repository
- [MATRIX](matrix.md) — how a repository classifies itself
- [WRITING](writing.md) — how the prose in this workspace is written
