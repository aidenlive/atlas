"""The compliance engine: the standards, enforced on a repository.

Every gate is a named :class:`Check` in a registry rather than a line in a shell
script. That buys three things a script could not offer:

* **Selection.** ``atlas check --only root-closed-set`` runs one gate, which is
  what you want while fixing one violation.
* **Reporting.** Each gate reports its id, the rule it enforces, and its
  violations, so ``--json`` output is structured rather than scraped.
* **Extension.** A team with a house rule registers a gate; it does not fork a
  growing shell script.

Gates are pure functions of the repository. They read, they never write, and
they return violations rather than printing or exiting, so the same code backs
the CLI, the tests, and the pre-commit hook. A gate that raises is reported as a
failed gate rather than taking the process down with it.

Every gate cites the rule it enforces. A gate that cannot name its rule is a
preference, and preferences do not belong in CI.
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import pathlib
import re
import tempfile
import typing as t

from ..paths import EXCLUDED_DIRS, Repository
from . import frontmatter, lexicon as lexicon_mod, lint as lint_mod, prompts as prompts_mod
from . import specs as specs_mod
from . import workstream as workstream_mod
from .manifest import Violation, load_yaml, validate_manifest

__all__ = ["Check", "CheckResult", "Report", "CHECKS", "register", "run", "check_ids"]

CheckFn = t.Callable[[Repository], list[Violation]]


@dataclasses.dataclass(frozen=True)
class Check:
    """One named compliance gate."""

    id: str
    summary: str
    rule: str
    run: CheckFn
    #: Gates that only make sense where the standards themselves are published.
    standards_only: bool = False


@dataclasses.dataclass
class CheckResult:
    check: Check
    violations: list[Violation]
    skipped: str | None = None

    @property
    def ok(self) -> bool:
        return self.skipped is not None or not self.violations

    @property
    def state(self) -> str:
        if self.skipped:
            return "skip"
        return "ok" if not self.violations else "fail"

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "id": self.check.id,
            "summary": self.check.summary,
            "rule": self.check.rule,
            "state": self.state,
            "skipped": self.skipped,
            "violations": [violation.as_dict() for violation in self.violations],
        }


@dataclasses.dataclass
class Report:
    repository: pathlib.Path
    results: list[CheckResult]

    @property
    def violations(self) -> list[Violation]:
        return [v for result in self.results for v in result.violations]

    @property
    def ok(self) -> bool:
        return not self.violations

    @property
    def passed(self) -> int:
        return sum(1 for result in self.results if result.state == "ok")

    @property
    def failed(self) -> int:
        return sum(1 for result in self.results if result.state == "fail")

    @property
    def skipped(self) -> int:
        return sum(1 for result in self.results if result.state == "skip")

    def as_dict(self) -> dict[str, t.Any]:
        return {
            "repository": str(self.repository),
            "ok": self.ok,
            "checks": [result.as_dict() for result in self.results],
            "summary": {
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
                "violations": len(self.violations),
            },
        }


CHECKS: dict[str, Check] = {}


def register(id: str, summary: str, rule: str, *, standards_only: bool = False):
    def decorate(fn: CheckFn) -> CheckFn:
        CHECKS[id] = Check(id=id, summary=summary, rule=rule, run=fn, standards_only=standards_only)
        return fn

    return decorate


def check_ids() -> list[str]:
    return list(CHECKS)


# ---------------------------------------------------------------------------
# The closed root (PROJECT PJ-01)
# ---------------------------------------------------------------------------

ROOT_FILES = frozenset(
    {
        "README.md", "LICENSE", "CHANGELOG.md", "AGENTS.md", "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md", "SECURITY.md", "ROADMAP.md",
        "project.yaml", "admin.yaml", "org.yaml",
        "CLAUDE.md", "GEMINI.md", ".cursorrules",
        "pyproject.toml", ".gitignore", ".editorconfig",
    }
)

ROOT_DIRS = frozenset(
    {
        ".git", ".github", "src", "tests", "docs", "work", "examples", "scripts",
        "ops", "assets", "library", "spec", "template", "packages",
    }
)

#: Directory names that are graveyards wherever they appear (PJ-09).
GRAVEYARDS = ("legacy", "old", "deprecated", "@removal-safe", "backup", "_old")

#: Documents whose whole job is duplicating truth that has a home (PJ-03).
REJECTED_ROOT_FILES = re.compile(r"^(INFO|STATUS|NOTES|TODO)\.md$|-STATUS\.md$", re.IGNORECASE)

#: Where prose lives, and therefore where declaration and linting apply.
DOCUMENT_DIRS = ("docs", "spec")

#: The seven sections PJ-11 requires of an agent guide.
AGENT_SECTIONS = (
    "purpose", "map", "commands", "conventions", "constraints", "definition of done", "pointers",
)

#: The README skeleton, in order (PJ-04, P-06).
README_SECTIONS = ("What", "Quickstart", "Documentation", "Status", "Contributing")


def _manifest(repo: Repository) -> dict[str, t.Any]:
    return load_yaml(repo.manifest_path) if repo.manifest_path.is_file() else {}


def _settings(repo: Repository) -> lint_mod.Settings:
    return lint_mod.Settings.from_manifest(_manifest(repo))


def _waived(repo: Repository, item: str) -> bool:
    """Is a checklist item waived, unexpired, in the manifest?

    A waiver is the standard's own escape hatch: it names the item, the reason,
    the approver, and an expiry. An expired waiver waives nothing.
    """
    today = dt.date.today()
    for waiver in _manifest(repo).get("waivers", []) or []:
        if not isinstance(waiver, dict) or waiver.get("item") != item:
            continue
        try:
            if dt.date.fromisoformat(str(waiver.get("expires"))) >= today:
                return True
        except (TypeError, ValueError):
            continue
    return False


# ---------------------------------------------------------------------------
# Manifests and classification
# ---------------------------------------------------------------------------


@register("manifest-valid", "project.yaml is present and schema-valid", "PROJECT PJ-12")
def _manifest_valid(repo: Repository) -> list[Violation]:
    if not repo.manifest_path.is_file():
        return [Violation(rule="PROJECT PJ-12", message="project.yaml is missing", path="project.yaml")]
    return validate_manifest(repo.manifest_path, repo.schema_dir, "project")


@register("matrix-classified", "All eight Matrix dimensions are classified", "MATRIX MX-01")
def _matrix(repo: Repository) -> list[Violation]:
    data = _manifest(repo)
    dimensions = ("type", "stage", "maturity", "packaging", "deploy", "ownership", "visibility", "support")
    violations = [
        Violation(rule="MATRIX MX-01", message=f"`{dimension}` is not classified", path="project.yaml")
        for dimension in dimensions
        if not data.get(dimension)
    ]

    if data.get("ownership") == "unowned":
        violations.append(
            Violation(
                rule="MATRIX MX-09",
                message="ownership is `unowned`, which is a defect, not a category",
                path="project.yaml",
                hint="legal only during a deprecated to archived transition, for at most 90 days",
            )
        )
    if data.get("stage") == "archived" and data.get("forge_archived") is not True:
        violations.append(
            Violation(
                rule="MATRIX MX-06",
                message="stage is `archived` but `forge_archived` is not true",
                path="project.yaml",
                hint="archive the repository on the forge; the state must be mechanically true",
            )
        )
    return violations


@register("admin-declared", "admin.yaml names who may act and who answers", "ADMIN I-1")
def _admin(repo: Repository) -> list[Violation]:
    if not repo.admin_path.is_file():
        return [
            Violation(
                rule="ADMIN I-1",
                message="admin.yaml is missing: no grant says who may act",
                path="admin.yaml",
                hint="copy template/admin.yaml and name the six duties",
            )
        ]
    violations = validate_manifest(repo.admin_path, repo.schema_dir, "admin")
    data = load_yaml(repo.admin_path)
    principals = {
        str(entry.get("id")): entry
        for entry in data.get("principals", []) or []
        if isinstance(entry, dict)
    }

    for duty, holder in (data.get("duties") or {}).items():
        if str(holder) not in principals:
            violations.append(
                Violation(
                    rule="ADMIN I-1",
                    message=f"duty `{duty}` is held by undeclared principal {holder!r}",
                    path="admin.yaml",
                )
            )

    today = dt.date.today()
    for identifier, entry in principals.items():
        if entry.get("kind") == "agent":
            if entry.get("role") in {"owner", "steward"}:
                violations.append(
                    Violation(
                        rule="ADMIN R-3",
                        message=f"agent {identifier} holds `{entry.get('role')}`",
                        path="admin.yaml",
                        hint="an agent can do a maintainer's work; it cannot answer for an organization",
                    )
                )
            if not entry.get("sponsor"):
                violations.append(
                    Violation(rule="ADMIN I-2", message=f"agent {identifier} names no human sponsor", path="admin.yaml")
                )
            if not entry.get("expires"):
                violations.append(
                    Violation(rule="ADMIN I-4", message=f"agent {identifier} has no expiry", path="admin.yaml")
                )
        expires = entry.get("expires")
        if expires:
            try:
                if dt.date.fromisoformat(str(expires)) < today:
                    violations.append(
                        Violation(
                            rule="ADMIN I-4",
                            message=f"{identifier} expired on {expires}",
                            path="admin.yaml",
                            hint="renew the grant deliberately, or remove the principal",
                        )
                    )
            except ValueError:
                violations.append(
                    Violation(rule="ADMIN I-4", message=f"{identifier} has a malformed expiry: {expires!r}", path="admin.yaml")
                )

    ownership = str(_manifest(repo).get("ownership", ""))
    if ownership and ownership != "unowned" and ownership not in principals:
        violations.append(
            Violation(
                rule="MATRIX MX-10",
                message=f"manifest ownership {ownership!r} is not a principal in admin.yaml",
                path="project.yaml",
                hint="one source of truth for who answers",
            )
        )
    return violations


@register("org-consistent", "org.yaml stays inside the steward bounds", "ADMIN R-4")
def _org(repo: Repository) -> list[Violation]:
    if not repo.org_path.is_file():
        return []
    violations = validate_manifest(repo.org_path, repo.schema_dir, "org")
    data = load_yaml(repo.org_path)
    stewards = data.get("stewards") or []
    if len(stewards) < 2:
        violations.append(Violation(rule="ADMIN R-4", message="fewer than two stewards: no bus factor", path="org.yaml"))
    if len(stewards) > 5:
        violations.append(
            Violation(
                rule="ADMIN R-4",
                message=f"{len(stewards)} stewards: a twelve-steward org has no stewards",
                path="org.yaml",
            )
        )
    return violations


# ---------------------------------------------------------------------------
# Repository shape
# ---------------------------------------------------------------------------


@register("root-closed-set", "The root contains only sanctioned entries", "PROJECT PJ-01")
def _root_closed_set(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for entry in sorted(repo.root.iterdir()):
        name = entry.name
        if entry.is_dir():
            if name in ROOT_DIRS or name in EXCLUDED_DIRS or name.startswith("."):
                continue
            violations.append(
                Violation(
                    rule="PROJECT PJ-01",
                    message=f"unsanctioned root directory: {name}/",
                    path=name,
                    hint="the root is a closed set; file it under an existing role directory",
                )
            )
        elif REJECTED_ROOT_FILES.match(name):
            violations.append(
                Violation(
                    rule="PROJECT PJ-03",
                    message=f"rejected status document: {name}",
                    path=name,
                    hint="the snapshot belongs in README.md and project.yaml; live status belongs in the tracker",
                )
            )
        elif name not in ROOT_FILES and not name.startswith("."):
            violations.append(
                Violation(
                    rule="PROJECT PJ-01",
                    message=f"unsanctioned root file: {name}",
                    path=name,
                    hint="the root is the first screen a stranger and an agent both see",
                )
            )
    return violations


@register("required-documents", "Every required root document exists", "PROJECT PJ-02")
def _required_documents(repo: Repository) -> list[Violation]:
    data = _manifest(repo)
    if data.get("stage") == "idea":
        return []
    required = ["README.md", "LICENSE", "CHANGELOG.md", "AGENTS.md", "CONTRIBUTING.md", "project.yaml"]
    violations = [
        Violation(rule="PROJECT PJ-02", message=f"{name} is missing", path=name)
        for name in required
        if not (repo.root / name).is_file()
    ]
    if data.get("visibility") == "public" and not (repo.root / "SECURITY.md").is_file():
        violations.append(
            Violation(rule="PROJECT PJ-02", message="SECURITY.md is required for a public repository", path="SECURITY.md")
        )
    return violations


@register("no-graveyards", "No in-repository graveyards", "PROJECT PJ-09")
def _graveyards(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for entry in sorted(repo.root.iterdir()):
        if not entry.is_dir() or entry.name not in GRAVEYARDS:
            continue
        if _waived(repo, "ST-01"):
            continue  # a dated, approved, expiring exception — see the waiver
        violations.append(
            Violation(
                rule="PROJECT PJ-09",
                message=f"graveyard directory: {entry.name}/",
                path=entry.name,
                hint="git is the archive; if one must exist, record a waiver with an expiry",
            )
        )
    return violations


@register("agent-guide", "One canonical agent guide, many pointers", "PROJECT PJ-11")
def _agent_guide(repo: Repository) -> list[Violation]:
    guide = repo.root / "AGENTS.md"
    if not guide.is_file():
        return [Violation(rule="PROJECT PJ-11", message="AGENTS.md is missing", path="AGENTS.md")]

    violations: list[Violation] = []
    text = guide.read_text(encoding="utf-8").lower()
    missing = [section for section in AGENT_SECTIONS if section not in text]
    if missing:
        violations.append(
            Violation(
                rule="PROJECT PJ-11",
                message="AGENTS.md is missing sections: " + ", ".join(missing),
                path="AGENTS.md",
                hint="purpose, map, commands, conventions, constraints, definition of done, pointers",
            )
        )

    for stub_name in ("CLAUDE.md", "GEMINI.md", ".cursorrules"):
        stub = repo.root / stub_name
        if not stub.is_file():
            continue
        lines = [line for line in stub.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(lines) > 3:
            violations.append(
                Violation(
                    rule="PROJECT PJ-11",
                    message=f"{stub_name} is {len(lines)} lines; a stub is three or fewer",
                    path=stub_name,
                )
            )
        if "AGENTS.md" not in "\n".join(lines):
            violations.append(
                Violation(rule="PROJECT PJ-11", message=f"{stub_name} does not point at AGENTS.md", path=stub_name)
            )
    return violations


@register("readme-composition", "The README follows the fixed skeleton", "PRESENTATION P-06")
def _readme(repo: Repository) -> list[Violation]:
    readme = repo.root / "README.md"
    if not readme.is_file():
        return [Violation(rule="PROJECT PJ-04", message="README.md is missing", path="README.md")]

    text = readme.read_text(encoding="utf-8")
    violations: list[Violation] = []
    first_screen = text.split("\n## ", 1)[0]

    if not any(marker in first_screen for marker in ("<picture", "<img", "![")):
        violations.append(
            Violation(
                rule="PRESENTATION P-02",
                message="the README opens with no hero visual",
                path="README.md",
                hint="a banner, screenshot, or diagram, in light and dark, with alt text",
            )
        )
    if "<img" in text and "alt=" not in text:
        violations.append(
            Violation(rule="PRESENTATION P-02", message="a README image carries no alt text", path="README.md")
        )

    headings = [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]
    for section in README_SECTIONS:
        if not any(heading.lower().startswith(section.lower()) for heading in headings):
            violations.append(
                Violation(
                    rule="PROJECT PJ-04",
                    message=f"README has no `{section}` section",
                    path="README.md",
                    hint="sections may be short; they may not be absent",
                )
            )

    description = str((_manifest(repo).get("metadata") or {}).get("description", "")).strip()
    if description:
        opening = "\n".join(text.splitlines()[:40]).lower()
        if description.rstrip(".").lower() not in opening:
            violations.append(
                Violation(
                    rule="PRESENTATION P-01",
                    message="the README's opening does not carry the manifest description",
                    path="README.md",
                    hint="one truth, two views",
                )
            )
    return violations


@register("presentation-metadata", "Forge metadata is declared in the manifest", "PRESENTATION P-01")
def _presentation(repo: Repository) -> list[Violation]:
    data = _manifest(repo)
    metadata = data.get("metadata") or {}
    if not metadata:
        return [Violation(rule="PRESENTATION P-01", message="no `metadata:` block in project.yaml", path="project.yaml")]

    violations: list[Violation] = []
    topics = metadata.get("topics") or []
    family = str(data.get("type", "")).split(".", 1)[0]
    if family and topics and topics[0] != family:
        violations.append(
            Violation(
                rule="PRESENTATION P-03",
                message=f"first topic is {topics[0]!r}; it must be the Matrix family {family!r}",
                path="project.yaml",
            )
        )
    if data.get("visibility") == "public" and not metadata.get("website"):
        violations.append(
            Violation(rule="PRESENTATION P-04", message="a public repository declares no website", path="project.yaml")
        )

    settings = repo.root / ".github" / "settings.yml"
    if settings.is_file():
        description = str(metadata.get("description", ""))
        if description and description not in settings.read_text(encoding="utf-8"):
            violations.append(
                Violation(
                    rule="PRESENTATION P-05",
                    message="forge settings have drifted from the manifest description",
                    path=".github/settings.yml",
                    hint="settings are applied from the manifest, never hand-typed",
                )
            )
    return violations


# ---------------------------------------------------------------------------
# The standards themselves
# ---------------------------------------------------------------------------


@register("spec-metadata", "Every standard declares its metadata", "PROJECT PJ-16", standards_only=True)
def _spec_metadata(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    specs = specs_mod.load_specs(repo.spec_dir)
    known = {spec.id for spec in specs}
    orders: dict[int, str] = {}
    for spec in specs:
        source = f"spec/{spec.path.name}"
        for field in specs_mod.REQUIRED_META:
            if not spec.meta.get(field):
                violations.append(
                    Violation(rule="PROJECT PJ-16", message=f"`{spec.id}` does not declare `{field}`", path=source)
                )
        if not spec.prefixes:
            violations.append(
                Violation(
                    rule="PROJECT PJ-16",
                    message=f"`{spec.id}` owns no identifier namespace",
                    path=source,
                    hint="a rule you cannot cite is a rule you cannot waive, review, or test",
                )
            )
        if spec.order in orders:
            violations.append(
                Violation(
                    rule="PROJECT PJ-16",
                    message=f"order {spec.order} is claimed by both `{orders[spec.order]}` and `{spec.id}`",
                    path=source,
                )
            )
        orders[spec.order] = spec.id
        for companion in spec.companions:
            if companion not in known:
                violations.append(
                    Violation(rule="PROJECT PJ-16", message=f"`{spec.id}` names an unknown companion: {companion}", path=source)
                )
    return violations


@register("rule-ids", "Rule identifiers are unique, owned, and gapless", "PROJECT PJ-16", standards_only=True)
def _rule_ids(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    seen: dict[str, str] = {}
    bold_id = re.compile(r"\*\*(?P<id>[A-Z]{1,3}-(?:[A-Z]\d{1,2}|\d{1,2}))\b")

    for spec in specs_mod.load_specs(repo.spec_dir):
        source = f"spec/{spec.path.name}"
        sequences: dict[str, list[int]] = {}
        for rule in spec.rules:
            namespace = next((p for p in spec.prefixes if rule.id.startswith(p)), None)
            if namespace is None:
                violations.append(
                    Violation(
                        rule="PROJECT PJ-16",
                        message=f"{rule.id} is not in a namespace `{spec.id}` declares",
                        path=source,
                        line=rule.line,
                    )
                )
                continue
            if rule.id in seen and seen[rule.id] != spec.id:
                violations.append(
                    Violation(
                        rule="PROJECT PJ-16",
                        message=f"{rule.id} is defined in both `{seen[rule.id]}` and `{spec.id}`",
                        path=source,
                        line=rule.line,
                    )
                )
            seen[rule.id] = spec.id
            tail = rule.id[len(namespace):]
            digits = re.sub(r"^[A-Z]", "", tail)
            if digits.isdigit():
                sequences.setdefault(namespace + re.sub(r"\d", "", tail), []).append(int(digits))

        for namespace, numbers in sequences.items():
            if numbers != list(range(1, len(numbers) + 1)):
                violations.append(
                    Violation(
                        rule="PROJECT PJ-16",
                        message=f"`{spec.id}` numbers {namespace} with a gap or a repeat: {numbers}",
                        path=source,
                        hint="a rule id is a permanent address; gaps invalidate citations",
                    )
                )

        # A rule the parser missed is a rule the tooling silently drops, which is
        # worse than a rule it rejects.
        declared = {rule.id for rule in spec.rules}
        for line_number, line in enumerate(spec.body.splitlines(), start=1):
            for match in bold_id.finditer(line):
                identifier = match.group("id")
                if identifier in declared or not any(identifier.startswith(p) for p in spec.prefixes):
                    continue
                violations.append(
                    Violation(
                        rule="PROJECT PJ-16",
                        message=f"{identifier} looks like a rule but did not parse as one",
                        path=source,
                        line=line_number,
                        hint="keep the bold title on one line",
                    )
                )
    return violations


# ---------------------------------------------------------------------------
# Library
# ---------------------------------------------------------------------------


@register("prompt-shape", "Every prompt asks for exactly one thing", "LIBRARY L-01")
def _prompt_shape(repo: Repository) -> list[Violation]:
    violations: list[Violation] = []
    for prompt in prompts_mod.load_prompts(repo.prompts_dir):
        relative = repo.relative(prompt.path)
        if prompt.sentences > prompts_mod.MAX_SENTENCES:
            violations.append(
                Violation(
                    rule="LIBRARY L-02",
                    message=f"{prompt.sentences} sentences (limit {prompts_mod.MAX_SENTENCES})",
                    path=relative,
                    hint="long procedure belongs in docs/guides/, referenced rather than inlined",
                )
            )
        if prompt.is_destructive and not prompt.has_guardrail:
            violations.append(
                Violation(
                    rule="LIBRARY L-04",
                    message="a destructive prompt with no guardrail in the sentence",
                    path=relative,
                    hint="plan before acting, or state the refusal condition",
                )
            )
        if prompt.path.name != f"request-{prompt.slug}.txt":
            violations.append(
                Violation(rule="LIBRARY L-07", message="filename is not request-<verb>-<object>.txt", path=relative)
            )
    return violations


@register("design-current", "The design system resolves, and its derivations are current", "LIBRARY L-A4")
def _design(repo: Repository) -> list[Violation]:
    """The fleet identity is consumed, never forked (P-11).

    Three claims, checked in order: the design file's front matter parses,
    every ``{group.token}`` reference in it resolves, and the artifacts derived
    from it — the generator tokens and the class index — match a regeneration.
    A repository without a design system skips cleanly; one with a stale
    derivation fails, because a drawn artifact that disagrees with its source
    is the visual form of a badge that disagrees with the manifest.
    """
    from . import design as design_mod

    source = repo.library_dir / "design" / "DESIGN.md"
    if not source.is_file():
        return []
    try:
        system = design_mod.load_design(source)
    except Exception as exc:  # noqa: BLE001 - the parse failure is the finding
        return [
            Violation(
                rule="LIBRARY L-A4",
                message=f"the design file's front matter does not parse: {exc}",
                path=repo.relative(source),
            )
        ]

    violations = [
        Violation(rule="LIBRARY L-A4", message=problem, path=repo.relative(source))
        for problem in design_mod.unresolved_references(system)
    ]

    derivations = (
        (repo.root / "assets" / "design" / "tokens.yaml", design_mod.render_tokens_yaml),
        (source.parent / "index.yaml", design_mod.render_index_yaml),
    )
    for target, render in derivations:
        if not target.is_file():
            violations.append(
                Violation(
                    rule="LIBRARY L-A4",
                    message=f"{target.name} has not been generated from the design system",
                    path=repo.relative(target),
                    hint="run `python scripts/build_design.py`",
                )
            )
        elif target.read_text(encoding="utf-8") != render(system):
            violations.append(
                Violation(
                    rule="LIBRARY L-A4",
                    message=f"{target.name} is out of date with the design system",
                    path=repo.relative(target),
                    hint="run `python scripts/build_design.py`, then the asset generators",
                )
            )
    return violations


@register("prompt-index", "The prompt index resolves in both directions", "LIBRARY L-08")
def _prompt_index(repo: Repository) -> list[Violation]:
    if not repo.prompts_dir.is_dir():
        return []
    index_path = repo.prompts_dir / "index.yaml"
    if not index_path.is_file():
        return [
            Violation(rule="LIBRARY L-08", message="library/prompts/index.yaml is missing", path="library/prompts/index.yaml")
        ]

    generated = prompts_mod.build_index(repo.prompts_dir)
    on_disk = load_yaml(index_path)
    violations: list[Violation] = []
    if generated.get("count") != on_disk.get("count"):
        violations.append(
            Violation(
                rule="LIBRARY L-08",
                message=f"index lists {on_disk.get('count')} prompts; {generated.get('count')} exist",
                path="library/prompts/index.yaml",
                hint="run `python scripts/build_library.py`",
            )
        )
    generated_ids = {p["id"] for stage in generated["categories"] for p in stage["prompts"]}
    indexed_ids = {
        p.get("id")
        for stage in (on_disk.get("categories") or [])
        for p in (stage.get("prompts") or [])
    }
    violations.extend(
        Violation(rule="LIBRARY L-08", message=f"indexed prompt does not exist: {ghost}", path="library/prompts/index.yaml")
        for ghost in sorted(indexed_ids - generated_ids)
    )
    violations.extend(
        Violation(rule="LIBRARY L-08", message=f"prompt is unindexed, and therefore invisible: {missing}", path="library/prompts/index.yaml")
        for missing in sorted(generated_ids - indexed_ids)
    )
    return violations


# ---------------------------------------------------------------------------
# Work
# ---------------------------------------------------------------------------


@register("workstreams-shaped", "Every workstream carries all nine sections", "WORKSTREAM W-05")
def _workstreams(repo: Repository) -> list[Violation]:
    return workstream_mod.validate_workstreams(repo.work_dir, repo.schema_dir)


@register("generated-current", "Generated views match their sources", "WORKSTREAM W-19")
def _generated_current(repo: Repository) -> list[Violation]:
    if not repo.work_dir.is_dir():
        return []
    violations: list[Violation] = []
    dashboard = repo.work_dir / "README.md"
    expected = workstream_mod.render_dashboard(repo.work_dir)
    if not dashboard.is_file():
        violations.append(
            Violation(rule="WORKSTREAM W-11", message="work/README.md has not been generated", path="work/README.md")
        )
    elif dashboard.read_text(encoding="utf-8").strip() != expected.strip():
        violations.append(
            Violation(
                rule="WORKSTREAM W-11",
                message="work/README.md is out of date with the task tables",
                path="work/README.md",
                hint="run `atlas work sync`",
            )
        )
    if not (repo.work_dir / "index.yaml").is_file():
        violations.append(
            Violation(
                rule="WORKSTREAM W-11",
                message="work/index.yaml has not been generated",
                path="work/index.yaml",
                hint="run `atlas work sync`",
            )
        )
    return violations


# ---------------------------------------------------------------------------
# Prose
# ---------------------------------------------------------------------------


@register("documents-declared", "Every document declares its facts", "WRITING WR-16")
def _documents_declared(repo: Repository) -> list[Violation]:
    settings = _settings(repo)
    violations: list[Violation] = []
    titles: dict[str, str] = {}
    for path in repo.walk_markdown(*DOCUMENT_DIRS):
        document = frontmatter.read(path)
        relative = repo.relative(path)
        if not document.has_frontmatter:
            violations.append(
                Violation(
                    rule="WRITING WR-16",
                    message="no front matter",
                    path=relative,
                    hint="declare " + ", ".join(settings.required_fields),
                )
            )
            continue
        for field in settings.required_fields:
            if not document.meta.get(field):
                violations.append(
                    Violation(rule="WRITING WR-16", message=f"front matter is missing `{field}`", path=relative)
                )

        # Two documents claiming one title is how a copy-paste error hides:
        # each file passes alone, and the reader meets the duplicate first.
        # One fact, one home (WR-15) applies to the documents themselves.
        title = str(document.meta.get("title", "")).strip().lower()
        if title:
            if title in titles:
                violations.append(
                    Violation(
                        rule="WRITING WR-15",
                        message=f"title {document.meta.get('title')!r} is also declared by {titles[title]}",
                        path=relative,
                        hint="two documents with one title are one document, or one is a stray copy",
                    )
                )
            else:
                titles[title] = relative

        review_by = document.meta.get("review_by")
        if not review_by:
            continue
        try:
            due = dt.date.fromisoformat(str(review_by))
        except ValueError:
            violations.append(
                Violation(rule="WRITING WR-16", message=f"`review_by` is not an ISO date: {review_by!r}", path=relative)
            )
        else:
            if due < dt.date.today():
                violations.append(
                    Violation(
                        rule="WRITING WR-16",
                        message=f"review was due {due.isoformat()}",
                        path=relative,
                        hint="re-read it, then move the date or supersede the document",
                    )
                )
    return violations


@register("links-resolve", "Every relative link points at something", "WRITING WR-14")
def _links(repo: Repository) -> list[Violation]:
    pattern = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")
    violations: list[Violation] = []
    for path in repo.walk_markdown():
        document = frontmatter.read(path)
        for index, line in enumerate(document.lines):
            for match in pattern.finditer(line):
                target = match.group("target")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if not (path.parent / target.split("#", 1)[0]).resolve().exists():
                    violations.append(
                        Violation(
                            rule="WRITING WR-14",
                            message=f"link target does not exist: {target}",
                            path=repo.relative(path),
                            line=document.line_number(index),
                        )
                    )
    return violations


@register("prose-lints-clean", "Published prose passes WRITING", "WRITING WR-01")
def _prose(repo: Repository) -> list[Violation]:
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    settings = _settings(repo)
    violations: list[Violation] = []
    for path in [repo.root / "README.md", *repo.walk_markdown(*DOCUMENT_DIRS)]:
        if not path.is_file():
            continue
        result = lint_mod.lint_document(frontmatter.read(path), lex, settings, skip=("declaration",))
        violations.extend(
            dataclasses.replace(finding.as_violation(), path=repo.relative(path)) for finding in result.errors
        )
    return violations


@register("lexicon-consistent", "The lexicon does not contradict itself", "WRITING WR-07")
def _lexicon(repo: Repository) -> list[Violation]:
    lex = lexicon_mod.load_lexicon(repo.lexicon_path)
    if not lex.terms and not lex.phrases:
        return []
    violations: list[Violation] = []
    relative = repo.relative(repo.lexicon_path)
    canonical = {term.use.lower(): term for term in lex.terms}
    seen: set[str] = set()
    for term in lex.terms:
        if term.id in seen:
            violations.append(Violation(rule="WRITING WR-07", message=f"duplicate term id {term.id!r}", path=relative))
        seen.add(term.id)
        for wrong in term.avoid:
            if wrong == term.use:
                violations.append(
                    Violation(
                        rule="WRITING WR-07",
                        message=f"term {term.use!r} lists its own canonical form under `avoid`",
                        path=relative,
                    )
                )
            other = canonical.get(wrong.lower())
            if other is not None and other.id != term.id:
                violations.append(
                    Violation(
                        rule="WRITING WR-07",
                        message=f"{wrong!r} is canonical for {other.id!r} and forbidden by {term.id!r}",
                        path=relative,
                    )
                )
    for phrase in lex.phrases:
        if not phrase.use:
            violations.append(
                Violation(
                    rule="WRITING WR-08",
                    message=f"phrase {phrase.avoid!r} has no replacement",
                    path=relative,
                    hint="a rule without a remedy is a complaint",
                )
            )
        if phrase.severity not in lexicon_mod.SEVERITIES:
            violations.append(
                Violation(
                    rule="WRITING WR-08",
                    message=f"phrase {phrase.avoid!r} has unknown severity {phrase.severity!r}",
                    path=relative,
                )
            )
    return violations


# ---------------------------------------------------------------------------
# Examples, waivers, and the template
# ---------------------------------------------------------------------------


@register("examples-valid", "Every worked example validates", "PROJECT PJ-10")
def _examples(repo: Repository) -> list[Violation]:
    directory = repo.root / "examples"
    if not directory.is_dir():
        return []
    from .manifest import detect_kind

    violations: list[Violation] = []
    for path in sorted(directory.glob("*.yaml")):
        violations.extend(
            dataclasses.replace(v, path=repo.relative(path))
            for v in validate_manifest(path, repo.schema_dir, detect_kind(path))
        )
    return violations


@register("waivers-honest", "Every waiver names a reason, an approver, and an expiry", "CHECKLIST ST-01")
def _waivers(repo: Repository) -> list[Violation]:
    today = dt.date.today()
    violations: list[Violation] = []
    for waiver in _manifest(repo).get("waivers", []) or []:
        if not isinstance(waiver, dict):
            continue
        item = waiver.get("item", "?")
        try:
            expires = dt.date.fromisoformat(str(waiver.get("expires")))
        except (TypeError, ValueError):
            violations.append(
                Violation(
                    rule="CHECKLIST ST-01",
                    message=f"waiver for {item} has no valid expiry",
                    path="project.yaml",
                    hint="a waiver without an expiry is a silent exception",
                )
            )
            continue
        if expires < today:
            violations.append(
                Violation(
                    rule="CHECKLIST ST-01",
                    message=f"waiver for {item} expired on {expires.isoformat()}",
                    path="project.yaml",
                    hint="renew it deliberately, or fix the item",
                )
            )
    return violations


@register("template-compliant", "The starter template passes what it teaches", "PROJECT PJ-01")
def _template(repo: Repository) -> list[Violation]:
    """Scaffold the template into a temporary directory and check *that*.

    Validating the template files in place would only prove that the
    placeholders parse. The claim worth making is that a repository somebody
    creates from this template passes on its first run, so the gate creates one.
    """
    if not repo.template_dir.is_dir():
        return []
    from . import template as template_mod

    with tempfile.TemporaryDirectory() as tmp:
        destination = pathlib.Path(tmp) / "scaffold-check"
        try:
            template_mod.scaffold(
                repo.template_dir,
                destination,
                name="scaffold-check",
                owner="team:standards",
                description="Scaffold verification run",
            )
        except Exception as exc:  # noqa: BLE001 - a broken template is the finding
            return [
                Violation(rule="PROJECT PJ-01", message=f"the template could not be scaffolded: {exc}", path="template/")
            ]

        report = run(Repository(root=destination), only=[c for c in CHECKS if c != "template-compliant"])
        return [
            dataclasses.replace(v, path=f"template/{v.path}" if v.path else "template/")
            for v in report.violations
        ]


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------


def run(repo: Repository, *, only: t.Sequence[str] | None = None) -> Report:
    from ..errors import NotFoundError

    selected = list(only) if only else list(CHECKS)
    for name in selected:
        if name not in CHECKS:
            raise NotFoundError(f"no check named {name!r}", hint=f"known checks: {', '.join(CHECKS)}")

    results: list[CheckResult] = []
    for name in selected:
        check = CHECKS[name]
        if check.standards_only and not repo.is_standards_source:
            results.append(CheckResult(check=check, violations=[], skipped="not the standards repository"))
            continue
        try:
            violations = check.run(repo)
        except Exception as exc:  # a broken gate is a failed gate, not a crash
            violations = [Violation(rule=check.rule, message=f"check raised {type(exc).__name__}: {exc}")]
        results.append(CheckResult(check=check, violations=violations))
    return Report(repository=repo.root, results=results)
