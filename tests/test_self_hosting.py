"""The suite passes the standard it defines."""

from __future__ import annotations

from atlas.core import compliance


def test_every_gate_passes(repo):
    report = compliance.run(repo)
    assert report.ok, "\n".join(str(v) for v in report.violations)


def test_no_gate_is_skipped_in_the_standards_repository(repo):
    assert compliance.run(repo).skipped == 0


def test_every_gate_cites_a_rule(repo):
    """A gate that cannot name its rule is a preference (ADR-0004)."""
    for check in compliance.CHECKS.values():
        assert check.rule, check.id
        standard, _, identifier = check.rule.partition(" ")
        assert standard.isupper(), check.id
        assert identifier, check.id


def test_every_cited_rule_exists(repo):
    from atlas.core import specs as specs_mod

    known = {rule.id for rule in specs_mod.all_rules(repo.spec_dir)}
    for check in compliance.CHECKS.values():
        identifier = check.rule.split(" ", 1)[1]
        assert identifier in known, f"{check.id} cites {identifier}, which no standard defines"


def test_gates_are_pure(repo):
    """Running the gates twice changes nothing on disk."""
    before = sorted(p.stat().st_mtime_ns for p in repo.root.rglob("*.md"))
    compliance.run(repo)
    assert sorted(p.stat().st_mtime_ns for p in repo.root.rglob("*.md")) == before


def test_a_broken_gate_is_reported_not_raised(repo, monkeypatch):
    def explode(_repo):
        raise RuntimeError("boom")

    monkeypatch.setitem(
        compliance.CHECKS,
        "manifest-valid",
        compliance.Check("manifest-valid", "x", "PROJECT PJ-12", explode),
    )
    report = compliance.run(repo, only=["manifest-valid"])
    assert not report.ok
    assert "boom" in report.violations[0].message


def test_duplicate_titles_are_detected(repo, tmp_path, monkeypatch):
    """The failure mode that motivated this: one file overwriting another leaves
    two documents declaring one title, each valid alone."""
    import shutil

    clone = tmp_path / "clone"
    shutil.copytree(repo.root, clone, ignore=shutil.ignore_patterns("@removal-safe", ".git", "__pycache__"))
    source = clone / "docs" / "reference" / "quick-reference.md"
    (clone / "docs" / "reference" / "stray-copy.md").write_text(
        source.read_text(encoding="utf-8"), encoding="utf-8"
    )
    from atlas.paths import Repository

    report = compliance.run(Repository(root=clone), only=["documents-declared"])
    assert any(v.rule == "WRITING WR-15" for v in report.violations)
