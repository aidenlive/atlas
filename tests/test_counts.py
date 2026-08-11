"""The counted claims in the prose match what the repository holds.

`scripts/build_counts.py` derives every count — standards, rules, gates,
prompts — from the same code the checks use and rewrites the claims in place.
This test applies the same rewrite and asserts nothing changes, so a hand-typed
number cannot drift past a green build.
"""

from __future__ import annotations

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _load_build_counts():
    spec = importlib.util.spec_from_file_location("build_counts", ROOT / "scripts" / "build_counts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_documented_counts_are_current() -> None:
    build_counts = _load_build_counts()
    n = build_counts.counts()
    stale = []
    for rel in build_counts.TARGETS:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if build_counts.rewrite(text, n) != text:
            stale.append(rel)
    assert not stale, f"stale counts in {stale}; run scripts/build_counts.py and commit"


def test_counts_are_plausible() -> None:
    build_counts = _load_build_counts()
    n = build_counts.counts()
    assert n["standards"] >= 9
    assert n["rules"] >= 200
    assert n["gates"] >= 24
    assert n["prompts"] >= 78
