"""Regression: the HTML reader must not collapse bold-lead-in lists into a paragraph.

The book style writes a bold label immediately followed by a list, with no blank
line between them:

    **触发分离的条件**：
    - 输入序列长度 > 某阈值

Strict CommonMark (pandoc's default `-f markdown`) requires a blank line before a
list, so it folds all three bullets into one <p>. build_html_reader.py therefore
must pass `markdown+lists_without_preceding_blankline`. This test feeds that exact
pattern through the *real* pandoc invocation the reader uses and asserts the list
survives — the check that would have caught the 640 collapsed lists that shipped.
"""

import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / "tools" / "build_html_reader.py"

# The pattern the book uses everywhere: bold lead-in, then a list, no blank line.
SAMPLE = "**触发分离的条件**：\n- 输入序列长度 > 某阈值\n- 输入序列未命中前缀缓存\n"


def _reader_pandoc_format() -> str:
    """Extract the pandoc `-f` value the reader uses, across every fork shape.

    Forks differ: an inline "-f", "markdown..." literal, a `reader = "markdown..."`
    variable, a `context="markdown..."` kwarg, or a PANDOC_MARKDOWN_READER constant
    living in tools/publication_sources.py (possibly as an implicitly-joined
    multiline string). Search both files and stitch adjacent string fragments.
    """
    texts = [READER.read_text(encoding="utf-8")]
    sources = READER.parent / "publication_sources.py"
    if sources.is_file():
        texts.append(sources.read_text(encoding="utf-8"))
    for src in texts:
        for pat in (
            r'"-f",\s*"(markdown[^"]*)"',
            r'reader\s*=\s*"(markdown[^"]*)"',
            r'context="(markdown[^"]*)"',
            # constant, one or more adjacent "..." fragments (implicit join)
            r'PANDOC_MARKDOWN_READER\s*=\s*\(?\s*((?:"[^"]*"\s*)+)\)?',
        ):
            m = re.search(pat, src)
            if m:
                raw = m.group(1)
                # collapse implicit string concatenation into one value
                return "".join(re.findall(r'"([^"]*)"', raw)) or raw
    raise AssertionError("could not find the reader's pandoc -f markdown format")


class HtmlListRenderingTests(unittest.TestCase):
    def test_reader_declares_the_no_blank_line_list_extension(self):
        fmt = _reader_pandoc_format()
        self.assertIn(
            "lists_without_preceding_blankline",
            fmt,
            "build_html_reader.py must enable lists_without_preceding_blankline; "
            f"pandoc format is currently {fmt!r}. Without it, every bold-lead-in "
            "list in the book collapses into a paragraph in the shipped HTML.",
        )

    def test_bold_lead_in_list_renders_as_ul_under_real_pandoc(self):
        pandoc = shutil.which("pandoc")
        if pandoc is None:
            self.skipTest("pandoc not installed; CI installs it and runs this check")
        fmt = _reader_pandoc_format()
        out = subprocess.run(
            [pandoc, "-f", fmt, "-t", "html5"],
            input=SAMPLE,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.assertIn("<ul>", out, f"list collapsed; pandoc -f {fmt} produced:\n{out}")
        self.assertEqual(out.count("<li>"), 2, f"expected 2 <li>; got:\n{out}")


if __name__ == "__main__":
    unittest.main()
