"""Atlas: declared, versioned, machine-checked structure for digital work.

Nine standards state what must be true of a body of work: where its files live,
what every repository contains, what kind of project it is, when it is good
enough, who may act, how it shows itself, where shared assets go, how the work
itself is planned and verified, and how all of it is written. The :mod:`atlas`
package checks a repository against them.

The package is a library first. Everything the CLI does can be imported from
:mod:`atlas.core` with no terminal involved, so one body of code serves the
command line, the test suite, CI, and whatever you build on top.
"""

from __future__ import annotations

#: Distribution version. Moves on every release of the tooling.
__version__ = "1.0.0"

#: The contract version of the standard the tooling enforces. Moves only when
#: the standard's requirements change. See docs/reference/versioning.md.
STANDARD = "project/1.0"

NAME = "atlas"

DESCRIPTION = "Declared, versioned, machine-checked structure for digital work"

__all__ = ["__version__", "STANDARD", "NAME", "DESCRIPTION"]
