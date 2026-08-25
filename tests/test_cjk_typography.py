#!/usr/bin/env python3
"""Guard the book's two Chinese-typography conventions.

Neither rule is enforced anywhere else: ``check_project_rules.py`` looks at
fences and links, ``check_emphasis.py`` at bold markers, and the workspace
``format_checker.py`` at quotes, fence languages and heading spacing. Intra-line
typography had no gate at all, and it drifted exactly as far as you would
expect -- one sibling book reached 45% unspaced CJK/Latin boundaries and another
reached a 50/50 split on parentheses, both mixed *within single files*. A
one-off sweep normalised all fourteen books; this file is what stops the next
paragraph from drifting back.

RULE 1 -- a CJK ideograph may not sit directly against ``[A-Za-z0-9]``.
         ``Harness的定义`` / ``第4章`` are violations; ``Harness 的定义`` is not.

RULE 2 -- a parenthesis whose content contains any CJK must be full-width.
         ``(用户命名空间映射)`` is a violation; ``（用户命名空间映射）`` is not.
         Latin-only parentheses are NOT touched: ``新建一个层 (Layer)`` and the
         ``项目(Agent)的经验`` hugging style both stay legal, because their
         content has no CJK.

Deliberately NOT checked, because the whole cluster agrees on the opposite:
Chinese punctuation against Latin (``（如 UI、监控服务）``) needs no space --
full-width punctuation already carries its own visual padding.

Everything a reader never sees as prose is excluded before the scan: fenced code
blocks and display-math blocks are skipped whole, and inline code, math, link
and image targets, HTML and bare URLs are replaced with Private Use Area
placeholders -- characters that can never themselves be mistaken for a letter, a
digit or an ideograph. Every mask pattern excludes that range in turn, because a
greedy ``\\S+`` will otherwise swallow the placeholder its predecessor just left
behind.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "_book", "node_modules", ".obsidian", "output", ".agent", "_site"}

PUA_FIRST = 0xE000
PUA = "\\ue000-\\uf8ff"
CJK = r"一-鿿㐀-䶿"
LATIN = r"A-Za-z0-9"

FENCE = re.compile(r"^\s*(?:```|~~~)")
MATH_BLOCK = re.compile(r"^\s*\$\$\s*$")
LINK_DEF = re.compile(r"^\s*\[[^\]]+\]:\s*\S+")

MASKS = (
    re.compile(r"<!--.*?-->"),
    re.compile(r"``[^`]+``"),
    re.compile(r"`[^`]*`"),
    re.compile(r"\$\$[^$]*\$\$"),
    # only treat $...$ as math when it actually contains math syntax, so that a
    # pair of prices ("$25/$125 per M tokens") is not read as one formula
    re.compile(r"\$(?=[^$\n]*[\\^_{])[^$\n]*\$"),
    re.compile(r"!?\]\([^)\s]*(?:\s+\"[^\"]*\")?\)"),
    # a real tag, not "| <1% | - | <5 | 各类GPU | >400ms |"
    re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*)?/?>"),
    re.compile("(?<![" + PUA + r"\w/])(?:https?|ftp)://[^\s" + PUA + "]+"),
)

ADJACENT = re.compile(f"[{CJK}][{LATIN}]|[{LATIN}][{CJK}]")
HALF_PAREN = re.compile(r"\([^()]*\)")


def mask(line: str) -> str:
    counter = [0]

    def repl(_match: "re.Match[str]") -> str:
        counter[0] += 1
        return chr(PUA_FIRST + counter[0] - 1)

    for pattern in MASKS:
        line = pattern.sub(repl, line)
    return line


def prose_lines(text: str):
    lines = text.split("\n")
    in_front = bool(lines) and lines[0].strip() == "---"
    in_fence = False
    in_math = False
    for number, line in enumerate(lines, start=1):
        if in_front:
            if number > 1 and line.strip() == "---":
                in_front = False
            continue
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if MATH_BLOCK.match(line):
            in_math = not in_math
            continue
        if in_math or LINK_DEF.match(line):
            continue
        yield number, line


def markdown_files(root: Path = ROOT):
    for path in sorted(root.rglob("*.md")):
        if SKIP_DIRS.isdisjoint(path.relative_to(root).parts):
            yield path


def unspaced(text: str):
    """RULE 1 violations."""
    for number, line in prose_lines(text):
        for match in ADJACENT.finditer(mask(line)):
            yield number, match.group(0), line.strip()[:100]


def half_width_parens(text: str):
    """RULE 2 violations."""
    for number, line in prose_lines(text):
        for match in HALF_PAREN.finditer(mask(line)):
            if re.search(f"[{CJK}]", match.group(0)):
                yield number, match.group(0)[:40], line.strip()[:100]


class CjkTypographyTests(unittest.TestCase):
    def test_cjk_and_latin_stay_apart(self) -> None:
        found = [
            f"{path.relative_to(ROOT)}:{number}: {hit!r} in {snippet}"
            for path in markdown_files()
            for number, hit, snippet in unspaced(path.read_text(encoding="utf-8"))
        ]
        self.assertEqual(
            [], found, "缺少中文与拉丁字符之间的半角空格：\n" + "\n".join(found[:40])
        )

    def test_parens_holding_chinese_are_full_width(self) -> None:
        found = [
            f"{path.relative_to(ROOT)}:{number}: {hit!r} in {snippet}"
            for path in markdown_files()
            for number, hit, snippet in half_width_parens(path.read_text(encoding="utf-8"))
        ]
        self.assertEqual(
            [], found, "含中文的括号应使用全角：\n" + "\n".join(found[:40])
        )

    def test_both_rules_can_actually_fail(self) -> None:
        """A check that cannot fail is not evidence."""
        self.assertEqual([], list(unspaced("使用 Harness 的记忆子系统。\n")))
        self.assertEqual(
            [(1, "s的", "使用 Harness的记忆子系统。")],
            list(unspaced("使用 Harness的记忆子系统。\n")),
        )
        self.assertEqual([(1, "第4", "第4 章")], list(unspaced("第4 章\n")))
        self.assertEqual([], list(half_width_parens("启用（用户命名空间映射）。\n")))
        self.assertEqual(
            [(1, "(用户命名空间映射)", "启用 (用户命名空间映射)。")],
            list(half_width_parens("启用 (用户命名空间映射)。\n")),
        )

    def test_latin_only_parens_are_left_alone(self) -> None:
        for sample in (
            "在基础镜像之上新建一个层 (Layer)。",
            "多个生产级智能体项目(Agent)的经验表明。",
            "定义一组相关联的应用容器为一个项目 (project)。",
        ):
            self.assertEqual([], list(half_width_parens(sample + "\n")), sample)

    def test_non_prose_regions_are_excluded(self) -> None:
        for sample in (
            "见 `mini_harness/核心.py` 说明。",
            "参考 [第 4 章的运行时](04_runtime/README.md)。",
            "地址是 https://example.com/中文path 这一条。",
            '<img src="a.png" alt="第4章示意图"> 的属性不算正文。',
            "见 [文档](a.md) https://e.com/x 结束。",
            "公式 $$L = (预测 - 真实)^2$$ 属于数学。",
            "记 $a^*$ 与 $O_t$ 为最优解。",
        ):
            self.assertEqual([], list(unspaced(sample + "\n")), sample)
            self.assertEqual([], list(half_width_parens(sample + "\n")), sample)

    def test_prices_are_not_mistaken_for_math(self) -> None:
        """A pair of '$' around prose must not mask the prose between them."""
        line = "定价 $25/$125 per M tokens，另有 $1 亿额度给 Glasswing计划。\n"
        self.assertEqual([(1, "g计", line.strip())], list(unspaced(line)))

    def test_html_text_content_is_still_prose(self) -> None:
        self.assertEqual(
            [(1, "文a", "<span>中文abc</span> 属于 HTML。")],
            list(unspaced("<span>中文abc</span> 属于 HTML。\n")),
        )

    def test_a_table_row_is_not_an_html_tag(self) -> None:
        line = "| 33-64 | 其他矿工 | <1% | - | <5 | 各类GPU | >400ms |\n"
        self.assertEqual([(1, "类G", line.strip())], list(unspaced(line)))

    def test_display_math_blocks_are_skipped_whole(self) -> None:
        text = "正文一行。\n\n$$\n\\text{原始Adam的权重衰减} = \\eta \\lambda \\theta\n$$\n\n正文二行。\n"
        self.assertEqual([], list(unspaced(text)))


if __name__ == "__main__":
    unittest.main()
