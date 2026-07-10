#!/usr/bin/env python3
"""Smoke-test built book artifacts and write a portable SHA-256 manifest."""

import argparse
import hashlib
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path


def fail(message):
    print(f"artifact verification failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalized_title(value):
    return " ".join(html.unescape(value).split())


def require_file(path):
    if not path.is_file():
        fail(f"{path} does not exist or is not a file")
    if path.stat().st_size == 0:
        fail(f"{path} is empty")


def verify_html(path, expected_title):
    require_file(path)
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<title(?:\s[^>]*)?>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    actual = normalized_title(match.group(1)) if match else ""
    expected = normalized_title(expected_title)
    accepted = actual == expected or actual.startswith(f"{expected} - ") or actual.endswith(f" - {expected}")
    if not accepted:
        fail(f"{path} title mismatch: expected {expected_title!r}, got {actual!r}")


def command_output(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"command failed ({' '.join(command)}): {(result.stderr or result.stdout).strip()}")
    return result.stdout


def verify_pdf(path, expected_title):
    require_file(path)
    if not path.read_bytes().startswith(b"%PDF-"):
        fail(f"{path} does not have a PDF signature")

    if shutil.which("pdfinfo") is None or shutil.which("pdftotext") is None:
        fail("pdfinfo and pdftotext are required for PDF title verification")

    metadata = command_output(["pdfinfo", str(path)])
    title_match = re.search(r"(?m)^Title:\s*(.*)$", metadata)
    metadata_title = normalized_title(title_match.group(1)) if title_match else ""
    expected = normalized_title(expected_title)
    if metadata_title == expected:
        return

    first_pages = normalized_title(
        command_output(["pdftotext", "-f", "1", "-l", "2", str(path), "-"])
    )
    if expected not in first_pages:
        fail(
            f"{path} title mismatch: expected {expected_title!r}; "
            f"PDF metadata title was {metadata_title!r}"
        )


def write_checksums(paths, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for path in sorted(paths, key=lambda item: item.name):
        if path.parent.resolve() != destination.parent.resolve():
            fail(f"{path} must be beside checksum manifest {destination}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.name}\n")
    destination.write_text("".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--site", type=Path)
    parser.add_argument("--checksums", type=Path)
    args = parser.parse_args()

    artifacts = []
    if args.pdf:
        verify_pdf(args.pdf, args.title)
        artifacts.append(args.pdf)
    if args.html:
        verify_html(args.html, args.title)
        artifacts.append(args.html)
    if args.site:
        verify_html(args.site / "index.html", args.title)
    if not artifacts and not args.site:
        parser.error("at least one of --pdf, --html, or --site is required")
    if args.checksums:
        if not artifacts:
            fail("a checksum manifest requires at least one file artifact")
        write_checksums(artifacts, args.checksums)

    for path in artifacts:
        print(f"verified artifact: {path}")
    if args.site:
        print(f"verified site: {args.site / 'index.html'}")
    if args.checksums:
        print(f"wrote checksums: {args.checksums}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
