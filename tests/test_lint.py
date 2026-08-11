"""The prose linter: each rule fires when it should, and stays quiet otherwise."""

from __future__ import annotations

import pathlib

import pytest

from atlas.core import frontmatter, lexicon as lexicon_mod, lint as lint_mod

CLEAN = """---
title: A clean document
kind: guide
owner: role:standards-maintainer
status: draft
updated: 2026-08-08
---

# A clean document

This document is short, declares itself, and has one title.

## A section

It links to the [install guide](install.md) by name.
"""


@pytest.fixture(scope="module")
def lex(repo):
    return lexicon_mod.load_lexicon(repo.lexicon_path)


def check(text: str, lex, **kw):
    return lint_mod.lint_document(frontmatter.parse(text, pathlib.Path("sample.md")), lex, **kw).findings


def fired(findings) -> set[str]:
    return {finding.check for finding in findings}


def test_a_clean_document_is_clean(lex):
    assert check(CLEAN, lex) == []


def test_missing_front_matter(lex):
    assert "declaration" in fired(check("# Title\n\nBody.\n", lex))


def test_missing_required_field(lex):
    assert any("owner" in f.message for f in check(CLEAN.replace("owner: role:standards-maintainer\n", ""), lex))


def test_second_h1(lex):
    assert "title" in fired(check(CLEAN + "\n# Another title\n", lex))


def test_h1_inside_a_code_fence_is_not_a_title(lex):
    assert "title" not in fired(check(CLEAN + "\n```bash\n# a shell comment\n```\n", lex))


def test_heading_jump(lex):
    assert "headings" in fired(check(CLEAN + "\n#### Too deep\n", lex))


def test_long_sentence_is_a_warning_not_an_error(lex):
    findings = [f for f in check(CLEAN + "\n" + ("word " * 50).strip() + ".\n", lex) if f.check == "sentence-length"]
    assert findings and all(f.severity == "warn" for f in findings)


def test_terminology_is_checked_against_the_lexicon(lex):
    assert "terminology" in fired(check(CLEAN + "\nWe host it on Github.\n", lex))


def test_canonical_spelling_passes(lex):
    assert "terminology" not in fired(check(CLEAN + "\nWe host it on GitHub.\n", lex))


def test_inline_code_is_exempt(lex):
    assert "terminology" not in fired(check(CLEAN + "\nRun `atlas check` now.\n", lex))


def test_urls_are_exempt(lex):
    """A link target is not prose; checking terminology inside one is noise."""
    assert "terminology" not in fired(check(CLEAN + "\nSee <https://github.com/OWNER/atlas>.\n", lex))


def test_the_same_word_is_reported_once(lex):
    assert len(check(CLEAN + "\nWe use Github daily.\n", lex, only=["terminology"])) == 1


def test_phrasing(lex):
    assert "phrasing" in fired(check(CLEAN + "\nWe utilize it in order to win.\n", lex))


def test_empty_link_text(lex):
    assert "links" in fired(check(CLEAN + "\nRead more [here](install.md).\n", lex))


def test_only_and_skip_select_rules(lex):
    text = "# No front matter\n\nWe utilize things.\n"
    assert fired(check(text, lex, only=["declaration"])) == {"declaration"}
    assert "declaration" not in fired(check(text, lex, skip=["declaration"]))


def test_unknown_rule_is_an_error(lex):
    from atlas.errors import NotFoundError

    with pytest.raises(NotFoundError):
        check(CLEAN, lex, only=["no-such-rule"])


def test_settings_come_from_the_manifest():
    settings = lint_mod.Settings.from_manifest({"lint": {"max_sentence_words": 12}})
    assert settings.max_sentence_words == 12
    assert settings.max_paragraph_sentences == lint_mod.Settings.max_paragraph_sentences


def test_every_lint_rule_cites_a_writing_rule():
    for name, (_summary, rule, _fn) in lint_mod.RULES.items():
        assert rule.startswith("WRITING WR-"), name
