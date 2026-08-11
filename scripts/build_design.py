#!/usr/bin/env python3
"""Regenerate everything derived from the design system.

``library/design/DESIGN.md`` is the source (L-A1). This script derives:

* ``assets/design/tokens.yaml`` — the small vocabulary the badge and terminal
  demo generators consume, in hex, both themes.
* ``library/design/index.yaml`` — the design class's index (L-A2).

Run it after any change to the design file, then re-run ``build_assets.py``
and ``build_screenshots.py`` so the drawn artifacts pick the change up. The
``design-current`` gate fails when any of this is stale.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from atlas.core import design  # noqa: E402


def main() -> int:
    source = ROOT / "library" / "design" / "DESIGN.md"
    system = design.load_design(source)

    problems = design.unresolved_references(system)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    tokens = ROOT / "assets" / "design" / "tokens.yaml"
    tokens.write_text(design.render_tokens_yaml(system), encoding="utf-8")
    print(f"wrote {tokens.relative_to(ROOT)}  ({system.name} v{system.version})")

    index = source.parent / "index.yaml"
    index.write_text(design.render_index_yaml(system), encoding="utf-8")
    print(f"wrote {index.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
