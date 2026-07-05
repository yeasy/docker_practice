#!/usr/bin/env python3
"""Prepare a temporary source tree for mdPress PDF builds.

mdPress assembles a single HTML document before printing it to PDF. Image paths
that are correct relative to their Markdown file, such as ../_images/foo.png,
can become incorrect in that assembled document. This script rewrites Markdown
and HTML image paths in a temporary copy so PDF builds can embed local assets
without changing source Markdown used by GitHub or HTML readers.
"""

import argparse
import base64
import mimetypes
import posixpath
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)([^)]*)\)")
HTML_IMAGE_RE = re.compile(r'(<img\b[^>]*\bsrc=)(["\'])([^"\']+)(\2)([^>]*>)', re.IGNORECASE)
SKIP_PREFIXES = ("http://", "https://", "/", "data:")


@dataclass(frozen=True)
class PrepareResult:
    markdown_files: int
    rewritten_paths: int


def _should_rewrite(url: str) -> bool:
    return bool(url) and not url.startswith(SKIP_PREFIXES)


def _normalize_url(reldir: str, url: str, book_dir: Path | None = None) -> str:
    normalized = posixpath.normpath(posixpath.join(reldir, url))
    if book_dir is None:
        return normalized
    target = (book_dir / normalized).resolve()
    if not target.is_file():
        return target.as_uri()
    media_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
    data = base64.b64encode(target.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{data}"


def normalize_markdown_asset_paths(text: str, reldir: str, book_dir: Path | None = None) -> tuple[str, int]:
    rewrites = 0

    def markdown_image(match: re.Match[str]) -> str:
        nonlocal rewrites
        alt, url, suffix = match.group(1), match.group(2).strip(), match.group(3)
        if not _should_rewrite(url):
            return match.group(0)
        rewrites += 1
        return f"![{alt}]({_normalize_url(reldir, url, book_dir)}{suffix})"

    def html_image(match: re.Match[str]) -> str:
        nonlocal rewrites
        prefix, quote, src, closing_quote, suffix = match.groups()
        if not _should_rewrite(src):
            return match.group(0)
        rewrites += 1
        return f"{prefix}{quote}{_normalize_url(reldir, src, book_dir)}{closing_quote}{suffix}"

    text = MARKDOWN_IMAGE_RE.sub(markdown_image, text)
    text = HTML_IMAGE_RE.sub(html_image, text)
    return text, rewrites


def _ignore_generated(_directory: str, names: list[str]) -> set[str]:
    ignored = {".git", "node_modules", "_book", "_site", "_site_site", "output", ".DS_Store"}
    return {name for name in names if name in ignored}


def prepare_pdf_sources(book_dir: Path, out_dir: Path) -> PrepareResult:
    book_dir = book_dir.resolve()
    out_dir = out_dir.resolve()
    if out_dir.exists():
        raise FileExistsError(f"output directory already exists: {out_dir}")

    shutil.copytree(book_dir, out_dir, ignore=_ignore_generated)

    markdown_files = 0
    rewritten_paths = 0
    for path in out_dir.rglob("*.md"):
        rel = path.relative_to(out_dir)
        if rel.parts and rel.parts[0] in {"_book", "_site", "_site_site"}:
            continue
        if rel.parent == Path("."):
            markdown_files += 1
            continue
        markdown_files += 1
        original = path.read_text(encoding="utf-8")
        normalized, count = normalize_markdown_asset_paths(original, rel.parent.as_posix(), out_dir)
        if count:
            path.write_text(normalized, encoding="utf-8")
            rewritten_paths += count

    return PrepareResult(markdown_files=markdown_files, rewritten_paths=rewritten_paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-dir", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    result = prepare_pdf_sources(args.book_dir, args.out)
    print(
        f"Prepared PDF sources at {args.out}: "
        f"{result.markdown_files} Markdown files, {result.rewritten_paths} image paths rewritten."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
