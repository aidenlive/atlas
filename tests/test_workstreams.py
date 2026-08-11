"""Workstreams: parsing, counting, generating, and validating."""

from __future__ import annotations

import shutil

import pytest

from atlas.core import workstream as ws_mod

TABLE = """
| ID | Task | Owner | Status |
|---|---|---|---|
| T-01 | Write it | person:a | done |
| T-02 | Review it | person:b | blocked |
"""


def test_nine_sections(repo):
    assert len(ws_mod.SECTIONS) == 9
    assert ws_mod.SECTIONS[0] == "01_plan"
    assert ws_mod.SECTIONS[-1] == "09_issues"


def test_task_table_parsing():
    tasks = ws_mod.parse_tasks(TABLE)
    assert [t.id for t in tasks] == ["T-01", "T-02"]
    assert tasks[0].done and not tasks[1].done


def test_progress_is_counted_not_claimed(repo):
    for workstream in ws_mod.load_workstreams(repo.work_dir):
        assert workstream.done == sum(1 for task in workstream.tasks if task.state == "done")


def test_dashboard_is_current(repo):
    rendered = ws_mod.render_dashboard(repo.work_dir)
    assert rendered.strip() == (repo.work_dir / "README.md").read_text(encoding="utf-8").strip()


def test_workstreams_validate(repo):
    assert ws_mod.validate_workstreams(repo.work_dir, repo.schema_dir) == []


def test_statuses_are_the_closed_enum(repo):
    for workstream in ws_mod.load_workstreams(repo.work_dir):
        assert workstream.status in ws_mod.STATUSES
        for task in workstream.tasks:
            assert task.state in ws_mod.TASK_STATES


def test_new_workstream_gets_all_nine_sections(repo, tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    shutil.copytree(repo.work_dir / "_template", work / "_template")
    created = ws_mod.create_workstream(work, "do-the-thing", owner="person:you")
    assert created.number == "01"
    for section in ws_mod.SECTIONS:
        assert (created.path / section).is_dir()


def test_numbers_do_not_collide(repo, tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    shutil.copytree(repo.work_dir / "_template", work / "_template")
    ws_mod.create_workstream(work, "one", owner="person:you")
    assert ws_mod.create_workstream(work, "two", owner="person:you").number == "02"


def test_a_bad_slug_is_rejected(repo, tmp_path):
    from atlas.errors import UsageError

    work = tmp_path / "work"
    work.mkdir()
    shutil.copytree(repo.work_dir / "_template", work / "_template")
    with pytest.raises(UsageError):
        ws_mod.create_workstream(work, "Not A Slug", owner="person:you")
