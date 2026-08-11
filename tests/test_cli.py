"""The command line: the parser, the reference it generates, and the exit codes."""

from __future__ import annotations

import json

import pytest

from atlas.cli import run_argv
from atlas.cli.app import GROUPS, MODULES, build_parser, command_tree, render_reference
from atlas.errors import ExitCode


def test_every_command_is_in_exactly_one_group():
    grouped = [name for _title, names in GROUPS for name in names]
    assert sorted(grouped) == sorted(MODULES)
    assert len(grouped) == len(set(grouped))


def test_the_command_surface_is_complete():
    """Twelve commands, one per thing a person does with a repository."""
    assert {"init", "status", "doctor", "check", "validate", "work", "spec",
            "prompt", "library", "site", "completion", "lint"} == set(MODULES)


def test_every_command_declares_a_summary_and_a_handler():
    for name, module in MODULES.items():
        assert module.SUMMARY and module.SUMMARY[0].islower(), name
        assert callable(module.run) and callable(module.configure)


def test_reference_matches_the_parser(root):
    generated = render_reference()
    on_disk = (root / "docs" / "reference" / "cli.md").read_text(encoding="utf-8")
    assert generated.split("# CLI reference", 1)[1] == on_disk.split("# CLI reference", 1)[1]


def test_reference_documents_every_command(root):
    text = (root / "docs" / "reference" / "cli.md").read_text(encoding="utf-8")
    for name in MODULES:
        assert f"### `atlas {name}`" in text


def test_global_flags_work_in_either_order():
    parser = build_parser()
    assert parser.parse_args(["--json", "check"]).json_mode is True
    assert parser.parse_args(["check", "--json"]).json_mode is True


def test_directory_flag_survives_the_subparser(root):
    assert build_parser().parse_args(["-C", str(root), "check"]).directory == str(root)


@pytest.mark.parametrize(
    "argv",
    [["check"], ["status"], ["spec", "list"], ["library", "list"], ["prompt", "list"], ["work", "list"]],
)
def test_commands_succeed_on_this_repository(root, argv):
    assert run_argv(["-C", str(root), *argv]) == ExitCode.OK


def test_nested_subcommands_accept_global_flags(root, capsys):
    for argv in (["spec", "rules", "--json"], ["--json", "spec", "rules"], ["work", "list", "--json"]):
        assert run_argv(["-C", str(root), *argv]) == ExitCode.OK
        json.loads(capsys.readouterr().out)


def test_json_output_is_parseable(root, capsys):
    run_argv(["-C", str(root), "--json", "check"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True and payload["summary"]["failed"] == 0


def test_not_a_repository_has_its_own_exit_code(tmp_path):
    assert run_argv(["-C", str(tmp_path), "check"]) == ExitCode.NOT_A_REPOSITORY


def test_unknown_check_is_not_found(root):
    assert run_argv(["-C", str(root), "check", "--only", "no-such-gate"]) == ExitCode.NOT_FOUND


def test_bare_invocation_prints_help(capsys):
    assert run_argv([]) == ExitCode.OK
    assert "commands:" in capsys.readouterr().out


def test_prompt_show_prints_only_the_prompt(root, capsys):
    run_argv(["-C", str(root), "prompt", "show", "cut-release"])
    assert "\n\n" not in capsys.readouterr().out.strip()


def test_output_counts_are_grammatical(root, capsys):
    run_argv(["-C", str(root), "--no-color", "check", "--only", "manifest-valid"])
    assert "1 gate passed" in capsys.readouterr().out


@pytest.mark.parametrize("argv", [["doctor"], ["check", "--list"], ["lint", "--list"], ["spec", "rules"]])
def test_informational_commands_run(root, argv):
    """`doctor` in particular reaches every Repository attribute it names."""
    assert run_argv(["-C", str(root), *argv]) in {ExitCode.OK, ExitCode.VIOLATIONS}
