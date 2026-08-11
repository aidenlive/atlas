"""Manifests, schemas, and worked examples."""

from __future__ import annotations

import json
import pathlib

import pytest

from atlas.core.manifest import KIND_SCHEMAS, detect_kind, validate_manifest


def test_project_manifest_is_valid(repo):
    assert validate_manifest(repo.manifest_path, repo.schema_dir, "project") == []


def test_admin_manifest_is_valid(repo):
    assert validate_manifest(repo.admin_path, repo.schema_dir, "admin") == []


@pytest.mark.parametrize("kind,filename", sorted(KIND_SCHEMAS.items()))
def test_every_schema_parses(repo, kind, filename):
    schema = json.loads((repo.schema_dir / filename).read_text(encoding="utf-8"))
    assert schema["$schema"].startswith("https://json-schema.org/")
    assert schema.get("title") and schema.get("description")


def test_examples_validate(repo):
    for path in sorted((repo.root / "examples").glob("*.yaml")):
        assert validate_manifest(path, repo.schema_dir, detect_kind(path)) == [], path.name


def test_detect_kind():
    assert detect_kind(pathlib.Path("admin.yaml")) == "admin"
    assert detect_kind(pathlib.Path("org.yaml")) == "org"
    assert detect_kind(pathlib.Path("a.workstream.yaml")) == "workstream"
    assert detect_kind(pathlib.Path("project.yaml")) == "project"


def test_matrix_enumerations_are_closed(repo, tmp_path):
    """MX-02: a value outside the enum fails validation."""
    bad = tmp_path / "project.yaml"
    bad.write_text(
        "standard: project/1.0\nname: x\ntype: service.telepathy\nstage: active\n"
        "maturity: stable\npackaging: none\ndeploy: none\nownership: team:x\n"
        "visibility: public\nsupport: none\n",
        encoding="utf-8",
    )
    violations = validate_manifest(bad, repo.schema_dir, "project")
    assert any("type" in v.message for v in violations)


def test_deprecated_requires_a_successor_and_a_date(repo, tmp_path):
    """MX-05, encoded in the schema rather than left to review."""
    bad = tmp_path / "project.yaml"
    bad.write_text(
        "standard: project/1.0\nname: x\ntype: tool.cli\nstage: deprecated\n"
        "maturity: stable\npackaging: none\ndeploy: none\nownership: team:x\n"
        "visibility: public\nsupport: none\n",
        encoding="utf-8",
    )
    assert validate_manifest(bad, repo.schema_dir, "project")


def test_a_bad_manifest_reports_every_error(repo, tmp_path):
    bad = tmp_path / "project.yaml"
    bad.write_text("standard: nope\nname: Not A Slug\n", encoding="utf-8")
    assert len(validate_manifest(bad, repo.schema_dir, "project")) >= 3
