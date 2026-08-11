"""Inspect the shared assets: prompts, icons, typefaces, media, and the lexicon.

LIBRARY makes reusable things first-class artifacts rather than attachments
somebody still has. This command reads them: what exists, what it is, and where
it came from. `atlas prompt` handles prompts specifically, because they are the
class people reach for by name.
"""

from __future__ import annotations

import argparse

from ...core import lexicon as lexicon_mod
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "inspect the shared assets: prompts, design, lexicon, and more"


def configure(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")

    subparsers.add_parser("list", help="show every asset class and what it holds")

    terms = subparsers.add_parser("terms", help="list the lexicon's terms")
    terms.add_argument("--kind", help="only terms of this kind")

    find = subparsers.add_parser("find", help="look a term up")
    find.add_argument("term", help="a word or part of one")

    subparsers.add_parser("phrases", help="list the phrases we replace")


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    subcommand = getattr(args, "subcommand", None) or "list"

    if subcommand == "list":
        return _classes(args, console, repo, lex)
    if subcommand == "terms":
        terms = [t for t in lex.terms if not args.kind or t.kind == args.kind]
        return _terms(console, terms, f"{len(terms)} terms")
    if subcommand == "find":
        terms = lex.find(args.term)
        if not terms:
            if console.json_mode:
                console.json([])
            else:
                console.state("info", f"nothing in the lexicon matches {args.term!r}")
            return int(ExitCode.NOT_FOUND)
        return _terms(console, terms, f"{len(terms)} matches")
    if subcommand == "phrases":
        if console.json_mode:
            console.json([phrase.as_dict() for phrase in lex.phrases])
            return int(ExitCode.OK)
        console.title(f"{len(lex.phrases)} phrases")
        console.out()
        for phrase in lex.phrases:
            console.out(f"  {phrase.avoid:<28}→  {phrase.use}")
            if phrase.reason:
                console.note(f"  {'':<28}   {phrase.reason}")
        return int(ExitCode.OK)
    raise UsageError(f"unknown subcommand: {subcommand}")


def _classes(args, console: Console, repo, lex) -> int:
    """What the library holds, one line per asset class (L-A2)."""
    from ...core import prompts as prompts_mod

    design_file = repo.library_dir / "design" / "DESIGN.md"
    counts = {
        "prompts": len(prompts_mod.load_prompts(repo.prompts_dir)),
        "lexicon": len(lex.terms) + len(lex.phrases),
        "design": 1 if design_file.is_file() else 0,
        "skills": len(list((repo.library_dir / "skills").glob("*/skill.yaml"))) if (repo.library_dir / "skills").is_dir() else 0,
        "icons": len(list((repo.library_dir / "icons").glob("*.svg"))) if (repo.library_dir / "icons").is_dir() else 0,
        "typefaces": len([p for p in (repo.library_dir / "typefaces").iterdir() if p.is_dir()]) if (repo.library_dir / "typefaces").is_dir() else 0,
        "media": len(list((repo.library_dir / "media").glob("*"))) if (repo.library_dir / "media").is_dir() else 0,
    }
    if console.json_mode:
        console.json(counts)
        return int(ExitCode.OK)
    console.title(f"library · {repo.relative(repo.library_dir)}")
    console.out()
    for name, count in counts.items():
        noun = "entry" if count == 1 else "entries"
        console.state("ok" if count else "skip", f"{name:<12}{count} {noun}")
    console.out()
    hints = ["`atlas prompt list`", "`atlas library terms`"]
    if counts["design"]:
        hints.append("library/design/DESIGN.md for the identity")
    console.note(" · ".join(hints))
    return int(ExitCode.OK)


def _terms(console: Console, terms, heading: str) -> int:
    if console.json_mode:
        console.json([term.as_dict() for term in terms])
        return int(ExitCode.OK)
    console.title(heading)
    console.out()
    for term in terms:
        console.out(f"  {term.use:<28}{term.kind}")
        if term.avoid:
            console.note(f"  {'':<28}not: {', '.join(term.avoid)}")
        if term.note:
            console.note(f"  {'':<28}{term.note}")
    return int(ExitCode.OK)
