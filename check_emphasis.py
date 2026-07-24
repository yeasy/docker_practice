#!/usr/bin/env python3
"""CJK-aware emphasis (bold/italic) renderability check for book repositories.

CommonMark only treats a run of ``*`` as an emphasis delimiter when it is
left/right-flanking. CJK punctuation counts as Unicode punctuation, so a closer
like ``**（配比）**相互交织`` is preceded by punctuation and followed by a letter:
it cannot close, and the page shows literal asterisks instead of bold. The
mirror case (``是**“引号”**``) cannot open. This gate flags such non-rendering
emphasis so each book's own CI catches a regression — the per-book
``check_project_rules.py`` only checks fences and local links.

This file is kept byte-for-byte identical across all book repos and mirrors
check 6 of the workspace-level ``format_checker.py``. Fix a flagged span by
inserting one space on the failing side (which book-rules 1.1 already asks for).
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {
    ".agent",
    ".git",
    ".github",
    ".mdpress",
    ".mypy_cache",
    ".pytest_cache",
    ".vuepress",
    "_book",
    "_site",
    "__pycache__",
    "dist",
    "mcp_cache",
    "node_modules",
    "output",
}

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
PUNCT_CATEGORIES = {"Pc", "Pd", "Pe", "Pf", "Pi", "Po", "Ps"}
ASCII_PUNCT = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
CJK_RE = re.compile(r"[㐀-鿿豈-﫿]")
ASTERISK_RUN_RE = re.compile(r"\*+")
BULLET_RE = re.compile(r"^(\s*(?:>\s*)*)([*+-])(\s+)")


def _fence_match(line: str):
    return FENCE_RE.match(line)


def _is_in_code_block(lines: list[str], line_idx: int) -> bool:
    active_char = ""
    active_len = 0
    for i in range(line_idx):
        match = _fence_match(lines[i])
        if not match:
            continue
        marker = match.group(1)
        char, length = marker[0], len(marker)
        if active_len == 0:
            active_char, active_len = char, length
        elif char == active_char and length >= active_len:
            active_char, active_len = "", 0
    return active_len > 0


def _is_in_mermaid_block(lines: list[str], line_idx: int) -> bool:
    active_char = ""
    active_len = 0
    is_mermaid = False
    for i in range(line_idx):
        match = _fence_match(lines[i])
        if not match:
            continue
        marker = match.group(1)
        char, length = marker[0], len(marker)
        if active_len == 0:
            active_char, active_len = char, length
            lang_parts = match.group(2).strip().split(maxsplit=1)
            is_mermaid = bool(lang_parts) and lang_parts[0].lower() == "mermaid"
        elif char == active_char and length >= active_len:
            active_char, active_len = "", 0
            is_mermaid = False
    return is_mermaid


def _is_punct(ch) -> bool:
    return ch is not None and (
        ch in ASCII_PUNCT or unicodedata.category(ch) in PUNCT_CATEGORIES
    )


def _is_space(ch) -> bool:
    return ch is None or ch.isspace()


def _left_flanking(prev_ch, next_ch) -> bool:
    if _is_space(next_ch):
        return False
    return (not _is_punct(next_ch)) or _is_space(prev_ch) or _is_punct(prev_ch)


def _right_flanking(prev_ch, next_ch) -> bool:
    if _is_space(prev_ch):
        return False
    return (not _is_punct(prev_ch)) or _is_space(next_ch) or _is_punct(next_ch)


def _neutralize_code(line: str) -> str:
    """Replace asterisks inside inline code / math / HTML with '+', preserving
    length and character classes. Only asterisks change: the backtick in
    ``**`x`**中文`` is itself punctuation and does affect whether the closer works,
    so the span must not be blanked wholesale."""

    def repl(match: re.Match) -> str:
        return match.group(0).replace("*", "+")

    for pattern in (r"`[^`]*`", r"\$\$[^$]*\$\$", r"<[^>]+>"):
        line = re.sub(pattern, repl, line)
    return line


def _scan_runs(line: str) -> list[dict]:
    runs = []
    for match in ASTERISK_RUN_RE.finditer(line):
        prev_ch = line[match.start() - 1] if match.start() else None
        next_ch = line[match.end()] if match.end() < len(line) else None
        runs.append(
            {
                "pos": match.start(),
                "len": len(match.group(0)),
                "n": len(match.group(0)),
                "orig": len(match.group(0)),
                "prev": prev_ch,
                "next": next_ch,
                "open": _left_flanking(prev_ch, next_ch),
                "close": _right_flanking(prev_ch, next_ch),
            }
        )
    return runs


def _process_emphasis(runs: list[dict]) -> list[dict]:
    """Run CommonMark's process-emphasis and return the delimiter runs that were
    left unpaired (they render as literal asterisks)."""
    ci = 0
    while ci < len(runs):
        closer = runs[ci]
        if not closer["close"] or closer["n"] == 0:
            ci += 1
            continue
        opener_i = None
        for oi in range(ci - 1, -1, -1):
            opener = runs[oi]
            if opener["n"] == 0 or not opener["open"]:
                continue
            if closer["open"] or opener["close"]:  # rule of three
                total = closer["orig"] + opener["orig"]
                if total % 3 == 0 and not (
                    closer["orig"] % 3 == 0 and opener["orig"] % 3 == 0
                ):
                    continue
            opener_i = oi
            break
        if opener_i is None:
            ci += 1
            continue
        opener = runs[opener_i]
        used = 2 if (opener["n"] >= 2 and closer["n"] >= 2) else 1
        opener["n"] -= used
        closer["n"] -= used
        for k in range(opener_i + 1, ci):
            runs[k]["n"] = 0
        if closer["n"] == 0:
            ci += 1
    return [run for run in runs if run["n"] > 0]


def _snippet(line: str, pos: int, width: int = 22) -> str:
    head = "…" if pos > width else ""
    tail = "…" if pos + width < len(line) else ""
    return head + line[max(0, pos - width):pos + width] + tail


def check_emphasis(line: str) -> list[str]:
    """Return descriptions of non-renderable emphasis markers on this line."""
    probe = _neutralize_code(line)
    probe = BULLET_RE.sub(lambda m: m.group(1) + "-" + m.group(3), probe)
    if "*" not in probe:
        return []

    runs = _scan_runs(probe)
    issues: list[str] = []

    # Rule 1: `**` come in pairs; odd ones should open, even ones should close.
    strong_runs = [run for run in runs if run["len"] >= 2]
    if strong_runs and len(strong_runs) % 2 == 0:
        for i, run in enumerate(strong_runs):
            if i % 2 == 0 and not run["open"]:
                why = (
                    "标记内侧有空格"
                    if _is_space(run["next"])
                    else "左邻文字、右邻标点，需在标记前补一个空格"
                )
                issues.append(
                    f"加粗开标记无法生效（{why}）: {_snippet(line, run['pos'])}"
                )
            elif i % 2 == 1 and not run["close"]:
                why = (
                    "标记内侧有空格"
                    if _is_space(run["prev"])
                    else "左邻标点、右邻文字，需在标记后补一个空格"
                )
                issues.append(
                    f"加粗闭标记无法生效（{why}）: {_snippet(line, run['pos'])}"
                )
        return issues

    # Rule 2: asterisks left over after pairing render literally.
    leftovers = _process_emphasis(runs)
    if len(leftovers) < 2:
        return issues  # a lone asterisk is usually a footnote mark, glob, or times sign
    has_strong = any(run["n"] >= 2 for run in leftovers)
    wraps_cjk = CJK_RE.search(line[leftovers[0]["pos"]:leftovers[-1]["pos"]])
    if has_strong or wraps_cjk:
        issues.append(f"强调标记无法渲染: {_snippet(line, leftovers[0]['pos'])}")
    return issues


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    files = iter_markdown_files()
    if not files:
        print("No Markdown files found; refusing to report success.")
        return 1
    issues: list[str] = []
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").split("\n")
        except OSError as exc:
            issues.append(f"{path.relative_to(ROOT)}:1: 读取文件失败: {exc}")
            continue
        for idx, line in enumerate(lines):
            if _is_in_code_block(lines, idx) or _is_in_mermaid_block(lines, idx):
                continue
            for description in check_emphasis(line):
                issues.append(f"{path.relative_to(ROOT)}:{idx + 1}: {description}")

    if issues:
        print("\n".join(issues))
        print(
            f"\n{len(issues)} emphasis issue(s) found across {len(files)} "
            "Markdown files. Fix by adding one space on the failing side "
            "of the ** markers."
        )
        return 1
    print(f"All {len(files)} Markdown files passed the emphasis check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
