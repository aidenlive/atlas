"""The design system: parsing, resolution, conversion, and derivation."""

from __future__ import annotations

import pytest

from atlas.core import design


@pytest.fixture(scope="module")
def system(repo):
    return design.load_design(repo.library_dir / "design" / "DESIGN.md")


def test_the_design_file_parses(system):
    assert system.name == "Neue"
    assert system.version == "1.0"
    for group in design.REQUIRED_GROUPS:
        assert group in system.data, group


def test_every_reference_resolves(system):
    assert design.unresolved_references(system) == []


def test_references_resolve_through_chains(system):
    """`on-background` → `{colors.on-surface}` → a literal."""
    resolved = design.resolve(system, "{colors.on-background}")
    assert resolved.startswith("oklch(")


def test_a_missing_reference_names_itself(system):
    with pytest.raises(ValueError, match="colors.no-such-token"):
        design.resolve(system, "{colors.no-such-token}")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("oklch(1 0 0)", "#FFFFFF"),
        ("oklch(0 0 0)", "#000000"),
        ("oklch(0.18 0 0 / 0.16)", None),  # alpha parses; ink is returned solid
    ],
)
def test_oklch_conversion_endpoints(value, expected):
    result = design.oklch_to_hex(value)
    if expected:
        assert result == expected
    assert len(result) == 7 and result.startswith("#")


def test_not_a_colour_is_rejected():
    with pytest.raises(ValueError):
        design.oklch_to_hex("#FFFFFF")


def test_generator_tokens_cover_both_themes(system):
    tokens = design.generator_tokens(system)
    for theme in ("light", "dark"):
        assert set(tokens["themes"][theme]) == set(design.THEME_ROLES)
        for value in tokens["themes"][theme].values():
            assert value.startswith("#") and len(value) == 7
    assert set(tokens["states"]) == set(design.STATE_ROLES)


def test_dark_ink_is_light_and_light_ink_is_dark(system):
    """The monochrome thesis, checked rather than trusted."""
    tokens = design.generator_tokens(system)

    def luma(value: str) -> int:
        return sum(int(value[i : i + 2], 16) for i in (1, 3, 5))

    assert luma(tokens["themes"]["light"]["text"]) < luma(tokens["themes"]["light"]["surface"])
    assert luma(tokens["themes"]["dark"]["text"]) > luma(tokens["themes"]["dark"]["surface"])


def test_the_derived_tokens_on_disk_are_current(repo, system):
    on_disk = (repo.root / "assets" / "design" / "tokens.yaml").read_text(encoding="utf-8")
    assert on_disk == design.render_tokens_yaml(system)


def test_the_design_index_is_current(repo, system):
    on_disk = (repo.library_dir / "design" / "index.yaml").read_text(encoding="utf-8")
    assert on_disk == design.render_index_yaml(system)


def test_the_site_stylesheet_carries_the_tokens(repo, system):
    from atlas.cli.commands import site

    css = site._style(repo)  # noqa: SLF001
    tokens = design.generator_tokens(system)
    assert tokens["themes"]["light"]["surface"] in css
    assert tokens["themes"]["dark"]["background"] in css
    assert "DM Sans" in css and "JetBrains Mono" in css
