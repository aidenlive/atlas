"""The design system, readable as data.

``library/design/DESIGN.md`` is the fleet's visual identity: normative YAML
front matter (tokens), then prose about applying them. PRESENTATION ``P-11``
says that identity lives once and is consumed, never forked — so this module is
the one place that reads it, and everything in this repository that draws
(badges, terminal demos, the rendered site) derives its values from here.

Three jobs:

* **Parse and resolve.** Front matter tokens may reference each other as
  ``{group.token}``. References resolve at build time and are never copied to a
  literal, which is what makes a re-theme a ramp swap rather than a hunt.
* **Convert.** Token colours are OKLCH. SVG renderers and older tooling want
  hex, so the conversion lives here, once.
* **Derive.** :func:`generator_tokens` maps design-system roles onto the small
  vocabulary the asset generators consume (``assets/design/tokens.yaml``), so
  the generators did not have to change when the design system arrived.
"""

from __future__ import annotations

import dataclasses
import math
import pathlib
import re
import typing as t

import yaml

__all__ = [
    "DesignSystem",
    "load_design",
    "resolve",
    "oklch_to_hex",
    "generator_tokens",
    "render_tokens_yaml",
    "render_index_yaml",
]

REFERENCE = re.compile(r"^\{(?P<group>[a-z][a-zA-Z-]*)\.(?P<token>[a-zA-Z0-9-]+)\}$")
OKLCH = re.compile(
    r"^oklch\(\s*(?P<l>[0-9.]+)\s+(?P<c>[0-9.]+)\s+(?P<h>[0-9.]+)"
    r"(?:\s*/\s*(?P<a>[0-9.]+))?\s*\)$"
)

#: The groups a build cannot proceed without. Everything else is optional
#: vocabulary a product may or may not use.
REQUIRED_GROUPS = ("colors", "typography", "spacing", "themes")


@dataclasses.dataclass(frozen=True)
class DesignSystem:
    """The parsed front matter, plus where it came from."""

    path: pathlib.Path
    name: str
    version: str
    data: dict[str, t.Any]

    @property
    def colors(self) -> dict[str, str]:
        return self.data.get("colors", {})

    @property
    def dark(self) -> dict[str, str]:
        """The dark theme's role overrides, flat, as the file declares them."""
        return {
            key: value
            for key, value in (self.data.get("themes", {}).get("dark", {}) or {}).items()
            if isinstance(value, str)
        }


def load_design(path: pathlib.Path) -> DesignSystem:
    """Read the design file's normative front matter.

    The file is front matter followed by prose; only the front matter carries
    values. A missing file raises — callers that treat the design system as
    optional check for the path first.
    """
    text = path.read_text(encoding="utf-8")
    front = text.split("\n---\n", 1)[0]
    data = yaml.safe_load(front)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: front matter is not a mapping")
    return DesignSystem(
        path=path,
        name=str(data.get("name", path.stem)),
        version=str(data.get("version", "?")),
        data=data,
    )


def resolve(system: DesignSystem, value: str, *, _seen: frozenset[str] = frozenset()) -> str:
    """Follow ``{group.token}`` references until a literal remains.

    A reference to a missing token, or a cycle, raises with the chain that got
    there — the failure a designer needs to see is *which* name is dangling.
    """
    match = REFERENCE.match(value.strip())
    if not match:
        return value
    key = f"{match.group('group')}.{match.group('token')}"
    if key in _seen:
        chain = " → ".join([*sorted(_seen), key])
        raise ValueError(f"reference cycle: {chain}")
    group = system.data.get(match.group("group"))
    if not isinstance(group, dict) or match.group("token") not in group:
        raise ValueError(f"unresolved reference {{{key}}}")
    return resolve(system, str(group[match.group("token")]), _seen=_seen | {key})


def unresolved_references(system: DesignSystem) -> list[str]:
    """Every dangling ``{group.token}`` in the file, as ``where: reference``."""
    problems: list[str] = []

    def walk(node: t.Any, trail: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{trail}.{key}" if trail else str(key))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{trail}[{index}]")
        elif isinstance(node, str) and REFERENCE.match(node.strip()):
            try:
                resolve(system, node)
            except ValueError as error:
                problems.append(f"{trail}: {error}")

    walk(system.data, "")
    return problems


# ---------------------------------------------------------------------------
# OKLCH → hex
# ---------------------------------------------------------------------------


def oklch_to_hex(value: str) -> str:
    """Convert an ``oklch(L C H)`` string to ``#rrggbb``.

    The standard OKLab pipeline: LCh → Lab → LMS → linear sRGB → gamma, with
    out-of-gamut channels clipped. Alpha, if present, is ignored — the callers
    of this function draw onto known surfaces and want the solid ink.
    """
    match = OKLCH.match(value.strip())
    if not match:
        raise ValueError(f"not an oklch() colour: {value!r}")
    lightness = float(match.group("l"))
    chroma = float(match.group("c"))
    hue = math.radians(float(match.group("h")))

    a = chroma * math.cos(hue)
    b = chroma * math.sin(hue)

    l_ = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3

    linear = (
        +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )

    def gamma(channel: float) -> int:
        channel = min(1.0, max(0.0, channel))
        srgb = 12.92 * channel if channel <= 0.0031308 else 1.055 * channel ** (1 / 2.4) - 0.055
        return round(min(1.0, max(0.0, srgb)) * 255)

    r, g, bl = (gamma(channel) for channel in linear)
    return f"#{r:02X}{g:02X}{bl:02X}"


def _hex(system: DesignSystem, token: str, *, dark: bool = False) -> str:
    """A colour role as hex, from the light table or the dark overrides."""
    if dark and token in system.dark:
        raw = system.dark[token]
    else:
        raw = system.colors[token]
    return oklch_to_hex(resolve(system, str(raw)))


# ---------------------------------------------------------------------------
# The generator vocabulary
# ---------------------------------------------------------------------------

#: Generator role → design-system role. One table, so the mapping is a fact a
#: reviewer can read rather than a scatter of lookups.
THEME_ROLES = {
    "background": "background",     # the field behind a card
    "surface": "surface",           # the card itself (terminal body, badge)
    "chrome": "surface-2",          # a window's title bar, recessed wells
    "border": "outline",            # hairline separation
    "text": "on-surface",
    "muted": "on-surface-3",
    "accent": "primary",            # Neue is monochrome: the accent is the ink
    "green": "success",
    "red": "error",
    "amber": "warning",
    "blue": "info",
}

#: Badge-dot roles. Neue reserves chroma for meaning, so each state borrows the
#: semantic colour that carries its meaning; the text beside the dot repeats the
#: state, so colour is never the only signal (P-05, AX-02).
STATE_ROLES = {
    "active": "success",
    "stable": "info",
    "release": "on-surface",        # monochrome brand: the release badge is ink
    "standard": "code-keyword",     # the one principled purple in the system
    "ci": "success",
    "license": "on-surface-3",
}


def generator_tokens(system: DesignSystem) -> dict[str, t.Any]:
    """The small token set the asset generators consume, derived from Neue."""
    typography = system.data.get("typography", {})
    body = typography.get("body-md", typography.get("body", {})) if isinstance(typography, dict) else {}
    sans = str(body.get("fontFamily", "DM Sans"))
    mono = "JetBrains Mono"

    return {
        "generated_by": "scripts/build_design.py",
        "source": "library/design/DESIGN.md",
        "system": system.name,
        "version": system.version,
        "themes": {
            "light": {role: _hex(system, token) for role, token in THEME_ROLES.items()},
            "dark": {role: _hex(system, token, dark=True) for role, token in THEME_ROLES.items()},
        },
        "states": {state: _hex(system, token) for state, token in STATE_ROLES.items()},
        "typography": {
            "sans": (
                f"'{sans}', "
                + ("'DM Sans', " if sans != "DM Sans" else "")
                + "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif"
            ),
            "mono": f"'{mono}', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
        },
    }


def render_tokens_yaml(system: DesignSystem) -> str:
    header = (
        "# Generated by scripts/build_design.py from library/design/DESIGN.md.\n"
        "# Do not edit: change the design system and re-run the script (L-A4).\n"
        "# Values are hex because SVG tooling reads them; the OKLCH originals\n"
        "# and the role mapping live with the source.\n"
    )
    return header + yaml.safe_dump(generator_tokens(system), sort_keys=False)


def render_index_yaml(system: DesignSystem) -> str:
    """The design class's index (L-A2), generated like the prompt index."""
    payload = {
        "generated_by": "scripts/build_design.py",
        "assets": [
            {
                "id": "design-system",
                "file": "DESIGN.md",
                "name": system.name,
                "version": system.version,
                "description": (
                    "The fleet's visual identity: tokens as normative front matter, "
                    "application prose after it. Consumed by the asset generators "
                    "and the site; never forked (P-11)."
                ),
            }
        ],
    }
    return "# Generated by scripts/build_design.py. Do not edit by hand.\n" + yaml.safe_dump(
        payload, sort_keys=False
    )
