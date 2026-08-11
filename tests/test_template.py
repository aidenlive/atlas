"""The starter template passes what it teaches."""

from __future__ import annotations

import pytest

from atlas.core import compliance, template as template_mod
from atlas.errors import UsageError
from atlas.paths import Repository


@pytest.fixture(scope="module")
def scaffolded(root, tmp_path_factory):
    destination = tmp_path_factory.mktemp("scaffold") / "invoice-api"
    template_mod.scaffold(
        root / "template", destination, name="invoice-api", owner="team:payments",
        description="Issues, stores, and reconciles customer invoices",
    )
    return Repository(root=destination)


def test_a_new_repository_passes_on_its_first_run(scaffolded):
    report = compliance.run(scaffolded)
    assert report.ok, "\n".join(str(v) for v in report.violations)


def test_no_placeholders_survive(scaffolded):
    for path in scaffolded.root.rglob("*"):
        if not path.is_file():
            continue
        leftover = [
            m.group(0)
            for m in template_mod.PLACEHOLDER.finditer(path.read_text(encoding="utf-8", errors="ignore"))
            if not m.group(0).startswith("{{WORKSTREAM")
        ]
        assert not leftover, (path, leftover)


def test_the_workstream_template_survives_scaffolding(scaffolded):
    tasks = (scaffolded.work_dir / "_template" / "02_tasks" / "tasks.md").read_text(encoding="utf-8")
    assert "{{WORKSTREAM_OWNER}}" in tasks


def test_a_scaffolded_repository_reads_the_packaged_standards(scaffolded):
    from atlas.core import specs as specs_mod

    assert not scaffolded.is_standards_source
    assert [s.id for s in specs_mod.load_specs(scaffolded.spec_dir)][:3] == ["workspace", "project", "matrix"]


def test_a_bad_name_is_rejected(root, tmp_path):
    with pytest.raises(UsageError):
        template_mod.scaffold(root / "template", tmp_path / "x", name="Not A Name", owner="team:x")
