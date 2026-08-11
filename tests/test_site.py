"""The site generator renders the Markdown this suite actually uses."""

from __future__ import annotations

from atlas.cli.commands import site


def test_headings_lists_and_code():
    html = site.render_markdown("# Title\n\nA paragraph.\n\n- one\n- two\n\n```bash\natlas check\n```\n")
    assert "<h1" in html and "<ul><li>one</li>" in html and "<pre><code" in html


def test_tables():
    html = site.render_markdown("| A | B |\n|---|---|\n| 1 | 2 |\n")
    assert "<table>" in html and "<th>A</th>" in html and "<td>2</td>" in html


def test_inline_formatting():
    html = site.render_markdown("Run `atlas check`, see the **rule**, read the [spec](spec.md).")
    assert "<code>atlas check</code>" in html
    assert "<strong>rule</strong>" in html
    assert '<a href="spec.md">spec</a>' in html


def test_html_is_escaped():
    assert "&lt;script&gt;" in site.render_markdown("A <script> tag in prose.")


def test_the_whole_suite_renders(repo, tmp_path):
    written = site.build(repo, tmp_path / "site")
    assert len(written) > 20
    assert (tmp_path / "site" / "index.html").is_file()
    assert (tmp_path / "site" / "spec" / "workspace.html").is_file()
    assert "WORKSPACE" in (tmp_path / "site" / "spec" / "workspace.html").read_text(encoding="utf-8")
