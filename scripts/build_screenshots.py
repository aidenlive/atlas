#!/usr/bin/env python3
"""Render the README's screenshots by running the real commands.

A hand-drawn mockup of terminal output is a claim nobody checked. These images
are produced by running `atlas` and capturing what it actually prints, so the
screenshot cannot show a result the tool does not produce (PUBLICATION P-07).

Output: `assets/demo-<name>-<theme>.svg`, one pair per demo.
"""

from __future__ import annotations

import html
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

#: Loaded from the design tokens at run time; this is only the fallback.
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
LINE_HEIGHT = 21
FONT_SIZE = 13.5
CHAR_WIDTH = 8.13
PAD_X, PAD_TOP, PAD_BOTTOM = 26, 56, 22

#: The demos, in the order the README uses them.
DEMOS: dict[str, tuple[str, list[str]]] = {
    # name: (window label, argv)
    "check": ("atlas check", ["check"]),
    "status": ("atlas status", ["status"]),
    "spec": ("atlas spec list", ["spec", "list"]),
}

def _load_themes() -> tuple[dict, str]:
    """The terminal palette, derived from the design system (P-11).

    ``tokens.yaml`` is generated from ``library/design/DESIGN.md`` by
    ``build_design.py``; nothing here names a colour directly. The window body
    is `surface` (a card), the title bar is `chrome`, and the state colours are
    the system's semantic set, so the demos re-theme when the design does.
    """
    tokens = yaml.safe_load((ASSETS / "design" / "tokens.yaml").read_text(encoding="utf-8"))
    themes = {}
    for name, table in tokens["themes"].items():
        themes[name] = {
            "bg": table["surface"],
            "chrome": table["chrome"],
            "border": table["border"],
            "text": table["text"],
            "muted": table["muted"],
            "green": table["green"],
            "red": table["red"],
            "amber": table["amber"],
            "blue": table["blue"],
        }
    return themes, tokens["typography"]["mono"]


THEMES, FONT = _load_themes()


def run(argv: list[str]) -> list[str]:
    """Run the CLI from this checkout and capture what a person would see."""
    result = subprocess.run(
        [sys.executable, "-m", "atlas", "--no-color", *argv],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin", "NO_COLOR": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + result.stderr).replace("\t", "    ")
    return [line.rstrip() for line in output.rstrip("\n").split("\n")]


def colour(line: str, theme: dict[str, str], *, is_title: bool = False) -> tuple[str, str]:
    """Decide a line's colour and weight from what it says, not from ANSI codes.

    The CLI never relies on colour to carry meaning, so the words are enough to
    recolour the transcript here.
    """
    stripped = line.strip()
    if is_title:
        return theme["text"], "500"
    if stripped.startswith("FAIL"):
        return theme["red"], "500"
    if stripped.startswith("ok"):
        return theme["green"], "400"
    if stripped.startswith("warn"):
        return theme["amber"], "400"
    if stripped.startswith("-"):
        # Findings carry their own severity word, so the transcript can tint
        # them the same way the terminal does.
        if " error " in stripped:
            return theme["red"], "400"
        if " warn " in stripped:
            return theme["amber"], "400"
        return theme["muted"], "400"

    if stripped.startswith(("$", "❯")):
        return theme["blue"], "500"
    return theme["text"], "400"


def render(lines: list[str], label: str, theme_name: str) -> str:
    theme = THEMES[theme_name]
    width = max(72, max((len(line) for line in lines), default=0) + 4)
    px_width = round(width * CHAR_WIDTH) + PAD_X * 2
    px_height = len(lines) * LINE_HEIGHT + PAD_TOP + PAD_BOTTOM

    rows = []
    for index, line in enumerate(lines):
        y = PAD_TOP + index * LINE_HEIGHT
        if not line.strip():
            continue
        fill, weight = colour(line, theme, is_title=not any(rows))
        leading = len(line) - len(line.lstrip(" "))
        x = PAD_X + round(leading * CHAR_WIDTH)
        rows.append(
            f'  <text x="{x}" y="{y}" fill="{fill}" font-weight="{weight}" '
            f'xml:space="preserve">{html.escape(line.strip())}</text>'
        )

    dots = "".join(
        f'<circle cx="{22 + i * 18}" cy="20" r="5.5" fill="{theme["border"]}"/>' for i in range(3)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{px_width}" height="{px_height}" viewBox="0 0 {px_width} {px_height}" role="img" aria-label="Terminal output of {html.escape(label)}">
  <title>{html.escape(label)}</title>
  <rect width="{px_width}" height="{px_height}" rx="10" fill="{theme["bg"]}" stroke="{theme["border"]}"/>
  <path d="M0 10a10 10 0 0 1 10-10h{px_width - 20}a10 10 0 0 1 10 10v30H0z" fill="{theme["chrome"]}"/>
  {dots}
  <text x="{px_width / 2}" y="25" fill="{theme["muted"]}" font-family="{FONT}" font-size="12" text-anchor="middle">{html.escape(label)}</text>
  <g font-family="{FONT}" font-size="{FONT_SIZE}">
{chr(10).join(rows)}
  </g>
</svg>
"""


def run_in(argv: list[str], cwd: pathlib.Path) -> list[str]:
    """Like :func:`run`, but against another repository (the scaffold demo)."""
    result = subprocess.run(
        [sys.executable, "-m", "atlas", "--no-color", *argv],
        cwd=cwd,
        env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin", "NO_COLOR": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + result.stderr).replace("\t", "    ")
    return [line.rstrip() for line in output.rstrip("\n").split("\n")]


def template_demo() -> None:
    """Record `atlas status` on a fresh scaffold, for the template README.

    The template teaches the pattern the root README follows (P-09): a real
    terminal transcript, not a mockup. Scaffolding first keeps the recording
    honest — it shows what a new repository actually prints (P-07).
    """
    import tempfile

    sys.path.insert(0, str(ROOT / "src"))
    from atlas.core import template as template_mod

    with tempfile.TemporaryDirectory() as tmp:
        destination = pathlib.Path(tmp) / "your-project"
        template_mod.scaffold(
            ROOT / "template",
            destination,
            name="your-project",
            owner="team:yours",
            description="A new repository from the starter template",
        )
        lines = run_in(["status"], destination)
    for theme in THEMES:
        target = ROOT / "template" / "docs" / "assets" / f"demo-status-{theme}.svg"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(lines, "atlas status", theme), encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}  ({len(lines)} lines)")


def main() -> int:
    manifest = yaml.safe_load((ROOT / "project.yaml").read_text(encoding="utf-8"))
    assert manifest["name"] == "atlas"

    for name, (label, argv) in DEMOS.items():
        lines = run(argv)
        for theme in THEMES:
            target = ASSETS / f"demo-{name}-{theme}.svg"
            target.write_text(render(lines, label, theme), encoding="utf-8")
            print(f"wrote {target.relative_to(ROOT)}  ({len(lines)} lines)")
    template_demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
