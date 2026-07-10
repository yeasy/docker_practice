#!/usr/bin/env python3
"""Validate the book's canonical container examples with their native tools."""

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "examples" / "validated"


@dataclass(frozen=True)
class Check:
    name: str
    executable: str
    command: List[str]
    probe: Optional[List[str]] = None


CHECKS = (
    Check(
        "docker compose",
        "docker",
        [
            "docker",
            "compose",
            "-f",
            str(FIXTURE_ROOT / "compose" / "compose.yaml"),
            "config",
            "--quiet",
        ],
        ["docker", "compose", "version"],
    ),
    Check(
        "docker buildx",
        "docker",
        [
            "docker",
            "buildx",
            "build",
            "--check",
            "--file",
            str(FIXTURE_ROOT / "dockerfile" / "Dockerfile"),
            str(FIXTURE_ROOT / "dockerfile"),
        ],
        ["docker", "buildx", "version"],
    ),
    Check(
        "kubeconform",
        "kubeconform",
        [
            "kubeconform",
            "-strict",
            "-summary",
            "-kubernetes-version",
            "1.31.0",
            str(FIXTURE_ROOT / "kubernetes" / "web.yaml"),
        ],
    ),
    Check(
        "actionlint",
        "actionlint",
        ["actionlint", str(FIXTURE_ROOT / "github-actions" / "validate.yml")],
    ),
)


def run_command(command):
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True)


def unavailable(check, require_tools, detail):
    status = "UNAVAILABLE" if require_tools else "SKIP"
    print(f"[{status}] {check.name}: {detail}")
    return require_tools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-tools",
        action="store_true",
        help="fail instead of skipping when a validator is unavailable (for CI)",
    )
    args = parser.parse_args()
    failed = False

    for check in CHECKS:
        if shutil.which(check.executable) is None:
            failed = unavailable(check, args.require_tools, f"{check.executable} not found") or failed
            continue

        if check.probe is not None:
            probe = run_command(check.probe)
            if probe.returncode != 0:
                detail = (probe.stderr or probe.stdout or "plugin probe failed").strip()
                failed = unavailable(check, args.require_tools, detail) or failed
                continue

        result = run_command(check.command)
        if result.returncode != 0:
            print(f"[FAIL] {check.name}")
            print((result.stderr or result.stdout).strip())
            failed = True
            continue

        print(f"[PASS] {check.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
