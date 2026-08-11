"""The prompt library and the lexicon."""

from __future__ import annotations

import yaml

from atlas.core import lexicon as lexicon_mod, prompts as prompts_mod

#: LIBRARY names fourteen categories as a closed set.
CATEGORIES = {
    "workspace", "repository", "architecture", "documentation", "github",
    "administration", "quality", "security", "releases", "maintenance",
    "design", "agents", "operations", "workstreams",
}


def test_the_categories_are_the_closed_set(repo):
    assert set(prompts_mod.stages(repo.prompts_dir)) == CATEGORIES


def test_the_prompt_catalog_is_complete(repo):
    assert len(prompts_mod.load_prompts(repo.prompts_dir)) == 78


def test_every_prompt_has_one_objective_and_three_sentences(repo):
    for prompt in prompts_mod.load_prompts(repo.prompts_dir):
        assert prompt.sentences <= prompts_mod.MAX_SENTENCES, prompt.slug
        assert "\n\n" not in prompt.text, prompt.slug


def test_destructive_prompts_carry_a_guardrail(repo):
    """L-04: a prompt that can be pasted carelessly must fail safe."""
    for prompt in prompts_mod.load_prompts(repo.prompts_dir):
        if prompt.is_destructive:
            assert prompt.has_guardrail, prompt.slug


def test_prompt_filenames_follow_the_convention(repo):
    for prompt in prompts_mod.load_prompts(repo.prompts_dir):
        assert prompt.path.name == f"request-{prompt.slug}.txt"


def test_index_resolves_in_both_directions(repo):
    generated = prompts_mod.build_index(repo.prompts_dir)
    on_disk = yaml.safe_load((repo.prompts_dir / "index.yaml").read_text(encoding="utf-8"))
    assert generated["count"] == on_disk["count"]
    assert [c["name"] for c in generated["categories"]] == [c["name"] for c in on_disk["categories"]]


def test_lexicon_loads_and_agrees_with_itself(repo):
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    assert lex.terms and lex.phrases
    assert all(phrase.use for phrase in lex.phrases)
    for term in lex.terms:
        assert term.use not in term.avoid
        assert term.severity in lexicon_mod.SEVERITIES


def test_a_missing_lexicon_is_not_an_error(tmp_path):
    lex = lexicon_mod.load_lexicon(tmp_path / "nope.yaml")
    assert lex.terms == () and lex.phrases == ()
