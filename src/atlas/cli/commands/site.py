"""Turn the standards and the documentation into a website you can read.

A deliberately small generator. It renders the Markdown this suite actually
uses — headings, paragraphs, lists, tables, code fences, blockquotes, links,
and inline formatting — into static HTML with no build step, no theme system,
and no dependency beyond the standard library.

The reason it exists at all: a standard nobody can read in a browser gets read
by nobody outside the repository. The reason it is small: a second rendering
pipeline is a second thing to maintain, and the Markdown remains canonical
(WORKSTREAM W-I2).
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import shutil
import typing as t

from ...core import frontmatter, specs as specs_mod
from ...errors import ExitCode, UsageError
from ...paths import discover
from ...terminal import Console

SUMMARY = "render the standards and docs as a static site"

#: Fallback palette, used only when the repository carries no design tokens.
#: When ``assets/design/tokens.yaml`` exists (generated from
#: ``library/design/DESIGN.md``), :func:`_style` substitutes its values, so the
#: site inherits the fleet identity rather than forking it (P-11).
FALLBACK = {
    "light": {
        "background": "#F3F3F3", "surface": "#FFFFFF", "chrome": "#F8F8F8",
        "border": "#E4E4E4", "text": "#121212", "muted": "#696969",
        "accent": "#121212", "blue": "#0064B9",
    },
    "dark": {
        "background": "#090909", "surface": "#121212", "chrome": "#181818",
        "border": "#292929", "text": "#F5F5F5", "muted": "#989898",
        "accent": "#F5F5F5", "blue": "#6DB6FF",
    },
    "sans": "'DM Sans', ui-sans-serif, system-ui, sans-serif",
    "mono": "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace",
}

STYLE_TEMPLATE = """\
:root {{ color-scheme: light dark;
  --bg:{l[background]}; --fg:{l[text]}; --muted:{l[muted]}; --line:{l[border]};
  --accent:{l[accent]}; --link:{l[blue]}; --code:{l[chrome]}; --card:{l[surface]}; }}
@media (prefers-color-scheme: dark) {{ :root {{
  --bg:{d[background]}; --fg:{d[text]}; --muted:{d[muted]}; --line:{d[border]};
  --accent:{d[accent]}; --link:{d[blue]}; --code:{d[chrome]}; --card:{d[surface]}; }} }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); line-height:1.6;
  font-family: {sans}; font-weight:400; }}
.wrap {{ display:grid; grid-template-columns: 260px minmax(0,1fr); gap:48px;
  max-width:1180px; margin:0 auto; padding:40px 24px; }}
nav {{ position:sticky; top:40px; align-self:start; font-size:14px;
  border-right:1px solid var(--line); padding-right:24px; }}
nav h2 {{ font-size:12px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--muted); margin:24px 0 8px; font-weight:500;
  font-family: {mono}; }}
nav a {{ display:block; padding:3px 0; color:var(--fg); text-decoration:none; }}
nav a:hover {{ color:var(--link); }}
main {{ min-width:0; background:var(--card); border:1px solid var(--line);
  padding:40px 48px; }}
h1, h2, h3 {{ font-weight:500; }}
h1 {{ font-size:32px; line-height:1.1; letter-spacing:-0.02em; margin:0 0 8px; }}
h2 {{ font-size:22px; margin:36px 0 12px; padding-top:12px;
  border-top:1px solid var(--line); }}
h3 {{ font-size:17px; margin:24px 0 8px; }}
p, li {{ font-size:16px; max-width:72ch; }}
a {{ color:var(--link); }}
strong {{ font-weight:500; }}
code {{ background:var(--code); padding:1px 5px;
  font-family: {mono}; font-size:.9em; }}
pre {{ background:var(--code); padding:14px 16px; overflow-x:auto;
  border:1px solid var(--line); }}
pre code {{ background:none; padding:0; }}
blockquote {{ margin:16px 0; padding:8px 18px; border-left:1px solid var(--accent);
  color:var(--muted); }}
table {{ border-collapse:collapse; width:100%; margin:16px 0; font-size:15px; }}
th, td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--line);
  vertical-align:top; }}
th {{ color:var(--muted); font-weight:500; font-size:13px;
  letter-spacing:.04em; text-transform:uppercase; font-family: {mono}; }}
.meta {{ color:var(--muted); font-size:13px; margin-bottom:28px;
  font-family: {mono}; }}
.badge {{ border:1px solid var(--line); padding:2px 9px; margin-right:6px;
  white-space:nowrap; }}
@media (max-width:820px) {{ .wrap {{ grid-template-columns:1fr; gap:16px; }}
  nav {{ position:static; border-right:0; padding-right:0; }}
  main {{ padding:24px 20px; }} }}
"""


def _style(repo) -> str:
    """The stylesheet, from the design tokens where the repository has them."""
    import yaml as yaml_mod

    light, dark = dict(FALLBACK["light"]), dict(FALLBACK["dark"])
    sans, mono = FALLBACK["sans"], FALLBACK["mono"]
    tokens_path = repo.root / "assets" / "design" / "tokens.yaml"
    if tokens_path.is_file():
        tokens = yaml_mod.safe_load(tokens_path.read_text(encoding="utf-8"))
        light.update(tokens.get("themes", {}).get("light", {}))
        dark.update(tokens.get("themes", {}).get("dark", {}))
        sans = tokens.get("typography", {}).get("sans", sans)
        mono = tokens.get("typography", {}).get("mono", mono)
    return STYLE_TEMPLATE.format(l=light, d=dark, sans=sans, mono=mono)

_INLINE = (
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])"), r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)"), r'<a href="\2">\1</a>'),
)


def configure(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="subcommand", metavar="<subcommand>")
    build = subparsers.add_parser("build", help="render the site into a directory")
    build.add_argument("--out", metavar="DIR", default="site", help="output directory (default: site)")
    serve = subparsers.add_parser("serve", help="build, then serve it locally")
    serve.add_argument("--out", metavar="DIR", default="site", help="output directory (default: site)")
    serve.add_argument("--port", type=int, default=8000, help="port to listen on (default: 8000)")


def run(args: argparse.Namespace, console: Console) -> int:
    repo = discover(args.directory)
    subcommand = getattr(args, "subcommand", None) or "build"
    if subcommand not in {"build", "serve"}:
        raise UsageError(f"unknown subcommand: {subcommand}", hint="build, serve")

    out = pathlib.Path(getattr(args, "out", "site"))
    if not out.is_absolute():
        out = repo.root / out
    written = build(repo, out)

    if console.json_mode:
        console.json({"output": str(out), "pages": len(written)})
    else:
        console.state("ok", f"rendered {len(written)} pages", repo.relative(out))

    if subcommand == "serve":
        return _serve(out, args.port, console)
    return int(ExitCode.OK)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    for pattern, replacement in _INLINE:
        out = pattern.sub(replacement, out)
    return out


def render_markdown(body: str) -> str:
    """Render the Markdown subset this suite uses.

    Not a general converter, and it does not pretend to be one: anything the
    standards do not use is passed through as a paragraph.
    """
    lines = body.splitlines()
    out: list[str] = []
    index = 0

    def close(tag: str) -> None:
        if out and out[-1].startswith(f"<{tag}"):
            out.pop()
        else:
            out.append(f"</{tag}>")

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            block: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                block.append(lines[index])
                index += 1
            attribute = f' class="language-{html.escape(language)}"' if language else ""
            out.append(f"<pre><code{attribute}>" + html.escape("\n".join(block)) + "</code></pre>")
            index += 1
            continue

        if not stripped:
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2)
            anchor = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{level} id="{anchor}">{inline(text)}</h{level}>')
            index += 1
            continue

        if stripped.startswith("|"):
            rows: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(lines[index].strip())
                index += 1
            out.append(_table(rows))
            continue

        if stripped.startswith(">"):
            quote: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote.append(lines[index].strip().lstrip(">").strip())
                index += 1
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            continue

        bullet = re.match(r"^\s*([-*+]|\d+\.)\s+(.*)$", line)
        if bullet:
            ordered = bullet.group(1).endswith(".")
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while index < len(lines):
                match = re.match(r"^\s*([-*+]|\d+\.)\s+(.*)$", lines[index])
                if match:
                    items.append(match.group(2))
                elif lines[index].startswith(("  ", "\t")) and lines[index].strip() and items:
                    items[-1] += " " + lines[index].strip()
                else:
                    break
                index += 1
            body_html = "".join(f"<li>{inline(item)}</li>" for item in items)
            out.append(f"<{tag}>{body_html}</{tag}>")
            continue

        if stripped.startswith("<"):
            out.append(stripped)
            index += 1
            continue

        paragraph: list[str] = []
        while index < len(lines) and lines[index].strip() and not re.match(
            r"^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|\||>|```|<)", lines[index]
        ):
            paragraph.append(lines[index].strip())
            index += 1
        if paragraph:
            out.append("<p>" + inline(" ".join(paragraph)) + "</p>")

    return "\n".join(out)


def _table(rows: list[str]) -> str:
    def cells(row: str) -> list[str]:
        return [cell.strip() for cell in row.strip().strip("|").split("|")]

    if not rows:
        return ""
    header = cells(rows[0])
    body = [cells(row) for row in rows[2:]] if len(rows) > 2 else []
    head_html = "".join(f"<th>{inline(cell)}</th>" for cell in header)
    body_html = "".join(
        "<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>" for row in body
    )
    return f"<table><thead><tr>{head_html}</tr></thead><tbody>{body_html}</tbody></table>"


def _page(title: str, meta: dict[str, t.Any], content: str, nav: str, depth: int) -> str:
    prefix = "../" * depth
    badges = "".join(
        f'<span class="badge">{html.escape(str(key))}: {html.escape(str(meta[key]))}</span>'
        for key in ("kind", "status", "owner", "updated")
        if meta.get(key)
    )
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Atlas</title>
<link rel="stylesheet" href="{prefix}style.css">
</head><body><div class="wrap">
<nav>{nav.replace('href="', f'href="{prefix}')}</nav>
<main><div class="meta">{badges}</div>
{content}
</main></div></body></html>
"""


def build(repo, out: pathlib.Path) -> list[pathlib.Path]:
    """Render every standard and document into ``out``."""
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "style.css").write_text(_style(repo), encoding="utf-8")

    pages: list[tuple[pathlib.Path, pathlib.Path, frontmatter.Document]] = []
    for source in [*repo.walk_markdown("spec"), *repo.walk_markdown("docs")]:
        relative = source.relative_to(repo.root).with_suffix(".html")
        pages.append((source, out / relative, frontmatter.read(source)))

    nav_parts = ['<h2>Standards</h2>']
    for spec in specs_mod.load_specs(repo.spec_dir):
        nav_parts.append(f'<a href="spec/{spec.path.stem}.html">{html.escape(spec.title.split(":")[0])}</a>')
    groups: dict[str, list[tuple[str, str]]] = {}
    for source, target, document in pages:
        parts = source.relative_to(repo.root).parts
        if parts[0] != "docs":
            continue
        groups.setdefault(parts[1] if len(parts) > 2 else "docs", []).append(
            (str(target.relative_to(out)), document.title)
        )
    for group, entries in sorted(groups.items()):
        nav_parts.append(f"<h2>{html.escape(group)}</h2>")
        nav_parts.extend(f'<a href="{href}">{html.escape(title)}</a>' for href, title in sorted(entries))
    nav = "\n".join(nav_parts)

    written: list[pathlib.Path] = []
    for source, target, document in pages:
        target.parent.mkdir(parents=True, exist_ok=True)
        content = render_markdown(re.sub(r"\.md(?=\)|#)", ".html", document.body))
        depth = len(target.relative_to(out).parts) - 1
        target.write_text(_page(document.title, document.meta, content, nav, depth), encoding="utf-8")
        written.append(target)

    index = repo.root / "README.md"
    if index.is_file():
        document = frontmatter.read(index)
        content = render_markdown(re.sub(r"\.md(?=\)|#)", ".html", document.body))
        (out / "index.html").write_text(_page("Atlas", {}, content, nav, 0), encoding="utf-8")
        written.append(out / "index.html")
    return written


def _serve(out: pathlib.Path, port: int, console: Console) -> int:  # pragma: no cover - blocking
    import functools
    import http.server

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        console.state("ok", f"serving on http://127.0.0.1:{port}", "ctrl-c to stop")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            console.out()
    return int(ExitCode.OK)
