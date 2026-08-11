"""The nine standards are readable as data, and their identifiers are sound."""

from __future__ import annotations

import re

import pytest

from atlas.core import specs as specs_mod

EXPECTED = [
    "workspace", "project", "matrix", "checklist", "admin",
    "presentation", "library", "workstream", "writing",
]

#: Every namespace `project/1.0` published. None of these may change: review
#: comments and commit messages already cite them (ADR-0002).
INHERITED = {
    "admin": ["I-", "R-"],
    "presentation": ["P-", "PR-"],
    "library": ["L-", "L-A", "L-I", "L-T", "L-M", "L-S"],
    "workstream": ["W-", "W-I", "WS-"],
    "checklist": [
        "AX-", "BD-", "CI-", "CL-", "DC-", "GA-", "GD-", "GX-", "HD-", "ID-",
        "OPS-", "QG-", "RL-", "SEC-", "ST-", "TS-",
    ],
}


def test_nine_standards_in_declared_order(repo):
    assert [spec.id for spec in specs_mod.load_specs(repo.spec_dir)] == EXPECTED


@pytest.mark.parametrize("field", specs_mod.REQUIRED_META)
def test_every_standard_declares_required_metadata(repo, field):
    for spec in specs_mod.load_specs(repo.spec_dir):
        assert spec.meta.get(field), f"{spec.id} is missing {field}"


@pytest.mark.parametrize("spec_id,prefixes", sorted(INHERITED.items()))
def test_inherited_namespaces_are_unchanged(repo, spec_id, prefixes):
    spec = specs_mod.find_spec(repo.spec_dir, spec_id)
    assert sorted(spec.rule_prefixes + spec.checklist_prefixes) == sorted(prefixes)


def test_the_three_previously_unnumbered_standards_now_carry_identifiers(repo):
    for spec_id, prefix in (("workspace", "WK-"), ("project", "PJ-"), ("matrix", "MX-")):
        spec = specs_mod.find_spec(repo.spec_dir, spec_id)
        assert spec.rule_prefixes == [prefix]
        assert spec.rules


def test_rules_are_gapless_within_each_namespace(repo):
    for spec in specs_mod.load_specs(repo.spec_dir):
        sequences: dict[str, list[int]] = {}
        for rule in spec.rules:
            namespace = next(p for p in spec.prefixes if rule.id.startswith(p))
            tail = rule.id[len(namespace):]
            sequences.setdefault(namespace + re.sub(r"\d", "", tail), []).append(
                int(re.sub(r"^[A-Z]", "", tail))
            )
        for namespace, numbers in sequences.items():
            assert numbers == list(range(1, len(numbers) + 1)), f"{spec.id} {namespace}"


def test_rule_ids_are_unique_across_the_suite(repo):
    ids = [rule.id for rule in specs_mod.all_rules(repo.spec_dir)]
    assert len(ids) == len(set(ids))


def test_every_rule_has_a_title(repo):
    for rule in specs_mod.all_rules(repo.spec_dir):
        assert rule.title.strip(), rule.id


def test_companions_exist(repo):
    known = {spec.id for spec in specs_mod.load_specs(repo.spec_dir)}
    for spec in specs_mod.load_specs(repo.spec_dir):
        assert set(spec.companions) <= known, spec.id


def test_the_parser_reads_every_identifier_shape(repo):
    """`I-1`, `WK-01`, `L-A1`, and `W-I1` are all real ids in the suite."""
    found = {rule.id for rule in specs_mod.all_rules(repo.spec_dir)}
    for identifier in ("I-1", "R-4", "WK-01", "PJ-16", "MX-10", "L-A1", "W-I1", "WS-01", "PR-06"):
        assert identifier in found
