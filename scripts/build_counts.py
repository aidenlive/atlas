#!/usr/bin/env python3
"""Rewrite the counted claims in the prose from what the repository holds.

"Nine standards", "24 gates", "78 prompts": every such number is a claim, and a
hand-typed claim drifts the day a standard, gate, or prompt is added. This
script derives each count from the same code the checks use and rewrites the
claims in place, so the prose is a view of the repository rather than a memory
of it (W-10: progress is counted, never claimed).

CI runs it with the other generators; a stale number fails the diff.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from atlas.core import compliance, lint as lint_mod, prompts as prompts_mod, specs as specs_mod  # noqa: E402

#: The documents whose counted claims this script owns.
TARGETS = (
    "README.md",
    "AGENTS.md",
    "library/README.md",
    "library/prompts/README.md",
    "docs/architecture/repository-design.md",
    "docs/reference/quick-reference.md",
    "docs/reference/glossary.md",
)

WORDS = {
    3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
    9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
    14: "fourteen", 15: "fifteen", 16: "sixteen", 20: "twenty",
    24: "twenty-four", 25: "twenty-five",
}

NUMBERISH = r"(?:\d+|" + "|".join(WORDS.values()) + r")"


def word(n: int) -> str:
    return WORDS.get(n, str(n))


def counts() -> dict[str, int]:
    specs = specs_mod.load_specs(ROOT / "spec")
    prompts = prompts_mod.load_prompts(ROOT / "library" / "prompts")
    categories = {p.stage for p in prompts}
    return {
        "standards": len(specs),
        "rules": sum(len(s.rules) for s in specs),
        "gates": len(compliance.check_ids()),
        "lint_rules": len(lint_mod.RULES),
        "prompts": len(prompts),
        "categories": len(categories),
    }


def rewrite(text: str, n: dict[str, int]) -> str:
    def cased(m: re.Match, value: str) -> str:
        return value.capitalize() if m.group(1)[:1].isupper() else value

    text = re.sub(
        rf"({NUMBERISH}) standards",
        lambda m: f"{cased(m, word(n['standards']))} standards",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(rf"{NUMBERISH} named gates", f"{word(n['gates'])} named gates", text, flags=re.IGNORECASE)
    text = re.sub(rf"\b\d+ gates\b", f"{n['gates']} gates", text)
    text = re.sub(r"\b\d+ rules and checklist items", f"{n['rules']} rules and checklist items", text)
    text = re.sub(r"\b\d+ rules from WRITING", f"{n['lint_rules']} rules from WRITING", text)
    text = re.sub(r"\b\d+ rules, run over", f"{n['lint_rules']} rules, run over", text)
    text = re.sub(r"\b\d+ written-once requests", f"{n['prompts']} written-once requests", text)
    text = re.sub(r"\b\d+ reusable request prompts", f"{n['prompts']} reusable request prompts", text)
    text = re.sub(r"\b\d+ prompts\b", f"{n['prompts']} prompts", text)
    text = re.sub(r"\b\d+ (lifecycle )?categories", lambda m: f"{n['categories']} {m.group(1) or ''}categories", text)
    return text


def main() -> int:
    n = counts()
    changed = 0
    for rel in TARGETS:
        path = ROOT / rel
        if not path.is_file():
            continue
        before = path.read_text(encoding="utf-8")
        after = rewrite(before, n)
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed += 1
            print(f"wrote {rel}")
    summary = ", ".join(f"{k}={v}" for k, v in n.items())
    print(f"counts: {summary} — {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
