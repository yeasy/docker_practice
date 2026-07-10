import json
import os
import re
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
FULL_ACTION_SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
TEST_REPOSITORY = "owner/repo"
TEST_SHA = "a" * 40
GET_REF_COMMAND = [
    "api",
    "--include",
    "--method",
    "GET",
    f"repos/{TEST_REPOSITORY}/git/ref/tags/preview-pdf",
]
PATCH_REF_COMMAND = [
    "api",
    "--silent",
    "--method",
    "PATCH",
    f"repos/{TEST_REPOSITORY}/git/refs/tags/preview-pdf",
    "--raw-field",
    f"sha={TEST_SHA}",
    "--field",
    "force=true",
]
POST_REF_COMMAND = [
    "api",
    "--silent",
    "--method",
    "POST",
    f"repos/{TEST_REPOSITORY}/git/refs",
    "--raw-field",
    "ref=refs/tags/preview-pdf",
    "--raw-field",
    f"sha={TEST_SHA}",
]
EDIT_RELEASE_COMMAND = [
    "release",
    "edit",
    "preview-pdf",
    "--title",
    "Latest Preview PDF",
    "--notes-file",
    "dist/release-notes.md",
    "--prerelease",
]
VIEW_RELEASE_COMMAND = ["release", "view", "preview-pdf"]
CREATE_RELEASE_COMMAND = [
    "release",
    "create",
    "preview-pdf",
    "--title",
    "Latest Preview PDF",
    "--notes-file",
    "dist/release-notes.md",
    "--prerelease",
    "--latest=false",
    "--verify-tag",
]

FAKE_GH = r'''#!/usr/bin/env python3
import json
import os
import sys

args = sys.argv[1:]
with open(os.environ["GH_LOG"], "a", encoding="utf-8") as stream:
    stream.write(json.dumps(args) + "\n")

scenario = os.environ["GH_SCENARIO"]
repository = "owner/repo"
sha = "a" * 40
reasons = {
    "401": "Unauthorized",
    "403": "Forbidden",
    "404": "Not Found",
    "429": "Too Many Requests",
    "503": "Service Unavailable",
}

def fail_http(code):
    print(f"HTTP/2.0 {code} {reasons[code]}")
    print(f"fake gh HTTP {code}", file=sys.stderr)
    raise SystemExit(1)

get_ref = ["api", "--include", "--method", "GET", f"repos/{repository}/git/ref/tags/preview-pdf"]
patch_ref = [
    "api", "--silent", "--method", "PATCH",
    f"repos/{repository}/git/refs/tags/preview-pdf",
    "--raw-field", f"sha={sha}", "--field", "force=true",
]
post_ref = [
    "api", "--silent", "--method", "POST", f"repos/{repository}/git/refs",
    "--raw-field", "ref=refs/tags/preview-pdf", "--raw-field", f"sha={sha}",
]
edit_release = [
    "release", "edit", "preview-pdf", "--title", "Latest Preview PDF",
    "--notes-file", "dist/release-notes.md", "--prerelease",
]
create_release = [
    "release", "create", "preview-pdf", "--title", "Latest Preview PDF",
    "--notes-file", "dist/release-notes.md", "--prerelease",
    "--latest=false", "--verify-tag",
]
view_release = ["release", "view", "preview-pdf"]

if os.environ.get("GH_REPO") != repository:
    print("fake gh requires explicit GH_REPO", file=sys.stderr)
    raise SystemExit(2)

if args == get_ref:
    if scenario.startswith("ref_network"):
        print("fake gh network failure", file=sys.stderr)
        raise SystemExit(1)
    for code in reasons:
        if scenario.startswith(f"ref_{code}"):
            fail_http(code)
    print("HTTP/2.0 200 OK")
    print('Content-Type: application/json\n\n{"ref":"refs/tags/preview-pdf"}')
    raise SystemExit(0)

if args in (patch_ref, post_ref, edit_release, create_release):
    raise SystemExit(0)

if args == view_release:
    if "release_missing" in scenario:
        print("release not found", file=sys.stderr)
        raise SystemExit(1)
    if "release_network" in scenario:
        print("fake release network failure", file=sys.stderr)
        raise SystemExit(1)
    for code in reasons:
        if f"release_{code}" in scenario:
            print(f"fake release HTTP {code}", file=sys.stderr)
            raise SystemExit(1)
    raise SystemExit(0)

print(f"unexpected gh argv: {args!r}", file=sys.stderr)
raise SystemExit(2)
'''


def workflow_step_script(workflow_text, step_name):
    marker = f"      - name: {step_name}\n"
    start = workflow_text.index(marker) + len(marker)
    run_marker = "        run: |\n"
    script_start = workflow_text.index(run_marker, start) + len(run_marker)
    script_end = workflow_text.find("\n      - name:", script_start)
    if script_end < 0:
        script_end = len(workflow_text)
    return textwrap.dedent(workflow_text[script_start:script_end])


class WorkflowSecurityTests(unittest.TestCase):
    @staticmethod
    def workflows():
        return sorted(WORKFLOW_DIR.glob("*.y*ml"))

    def test_all_actions_are_immutable_with_version_comments(self):
        failures = []
        for workflow in self.workflows():
            for number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), 1):
                match = re.search(r"\buses:\s*([^\s#]+)(?:\s+#\s*(\S+))?", line)
                if not match:
                    continue
                action, version = match.groups()
                if not FULL_ACTION_SHA.fullmatch(action) or not version or not version.startswith("v"):
                    failures.append(f"{workflow.name}:{number}: {line.strip()}")
        self.assertEqual(failures, [])

    def test_checkout_never_persists_credentials(self):
        failures = []
        for workflow in self.workflows():
            lines = workflow.read_text(encoding="utf-8").splitlines()
            for index, line in enumerate(lines):
                if "uses: actions/checkout@" not in line:
                    continue
                step = "\n".join(lines[index : index + 8])
                if "persist-credentials: false" not in step:
                    failures.append(f"{workflow.name}:{index + 1}")
        self.assertEqual(failures, [])

    def test_every_workflow_declares_permissions(self):
        failures = []
        for workflow in self.workflows():
            text = workflow.read_text(encoding="utf-8")
            before_jobs = text.split("\njobs:", 1)[0]
            if not re.search(r"(?m)^permissions:", before_jobs):
                failures.append(workflow.name)
        self.assertEqual(failures, [])

    def test_release_and_preview_separate_read_only_builds_from_writes(self):
        expectations = {
            "auto-release.yml": ("release",),
            "preview-pdf.yml": ("publish",),
        }
        for name, write_jobs in expectations.items():
            text = (WORKFLOW_DIR / name).read_text(encoding="utf-8")
            self.assertRegex(text, r"(?ms)^  build:\n    permissions:\n      contents: read\b", name)
            for job in write_jobs:
                self.assertRegex(
                    text,
                    rf"(?ms)^  {job}:.*?permissions:\n      contents: write\b.*?needs: build\b",
                    name,
                )

    def run_preview_scripts(
        self,
        scenario,
        *,
        repository=TEST_REPOSITORY,
        sha=TEST_SHA,
    ):
        preview = (WORKFLOW_DIR / "preview-pdf.yml").read_text(encoding="utf-8")
        scripts = (
            workflow_step_script(preview, "Synchronize mutable preview tag"),
            workflow_step_script(preview, "Create or update preview release"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_gh = root / "gh"
            fake_gh.write_text(FAKE_GH, encoding="utf-8")
            fake_gh.chmod(0o755)
            log = root / "commands.jsonl"
            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{root}:{env.get('PATH', '')}",
                    "GH_LOG": str(log),
                    "GH_SCENARIO": scenario,
                    "GH_TOKEN": "test-token",
                    "GH_REPO": repository,
                    "GITHUB_REPOSITORY": repository,
                    "GITHUB_SHA": sha,
                }
            )
            result = None
            for script in scripts:
                result = subprocess.run(
                    ["/bin/bash", "-c", script],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    break
            commands = []
            if log.exists():
                commands = [
                    json.loads(line)
                    for line in log.read_text(encoding="utf-8").splitlines()
                ]
            return result, commands

    def test_mutable_preview_updates_existing_tag_and_release(self):
        result, commands = self.run_preview_scripts("ref_200_release_exists")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            commands,
            [GET_REF_COMMAND, PATCH_REF_COMMAND, VIEW_RELEASE_COMMAND, EDIT_RELEASE_COMMAND],
        )

    def test_mutable_preview_creates_only_on_explicit_not_found(self):
        result, commands = self.run_preview_scripts("ref_404_release_missing")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            commands,
            [GET_REF_COMMAND, POST_REF_COMMAND, VIEW_RELEASE_COMMAND, CREATE_RELEASE_COMMAND],
        )
        flattened = [argument for command in commands for argument in command]
        self.assertNotIn("--target", flattened)

    def test_preview_rejects_invalid_repository_and_sha_before_calling_gh(self):
        cases = (
            {"repository": "owner/repo/extra", "sha": TEST_SHA, "message": "Invalid GITHUB_REPOSITORY"},
            {"repository": TEST_REPOSITORY, "sha": "a" * 39, "message": "Invalid GITHUB_SHA"},
        )
        for case in cases:
            with self.subTest(case=case):
                result, commands = self.run_preview_scripts(
                    "ref_200_release_exists",
                    repository=case["repository"],
                    sha=case["sha"],
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(commands, [])
                self.assertIn(case["message"], result.stderr)

    def test_preview_tag_lookup_fails_closed_on_non_404_errors(self):
        for scenario in ("ref_401", "ref_403", "ref_429", "ref_503", "ref_network"):
            with self.subTest(scenario=scenario):
                result, commands = self.run_preview_scripts(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(commands, [GET_REF_COMMAND])
                expected = "network failure" if scenario.endswith("network") else scenario.removeprefix("ref_")
                self.assertIn(expected, result.stderr)

    def test_preview_release_lookup_fails_closed_except_exact_not_found(self):
        scenarios = (
            "ref_200_release_401",
            "ref_200_release_403",
            "ref_200_release_404",
            "ref_200_release_429",
            "ref_200_release_503",
            "ref_200_release_network",
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                result, commands = self.run_preview_scripts(scenario)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(
                    commands,
                    [GET_REF_COMMAND, PATCH_REF_COMMAND, VIEW_RELEASE_COMMAND],
                )
                expected = "network failure" if scenario.endswith("network") else scenario.rsplit("release_", 1)[1]
                self.assertIn(expected, result.stderr)

    def test_preview_publish_has_explicit_repo_context_only_in_write_job(self):
        preview = (WORKFLOW_DIR / "preview-pdf.yml").read_text(encoding="utf-8")
        build, publish = preview.split("\n  publish:\n", 1)

        self.assertNotIn("GH_REPO", build)
        self.assertIn("GH_REPO: ${{ github.repository }}", publish)

    def test_downloads_dependencies_and_link_checker_are_integrity_pinned(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in self.workflows())
        link_text = (WORKFLOW_DIR / "check-link.yml").read_text(encoding="utf-8")

        self.assertNotRegex(combined, r"npm install\s+-g\s+@mermaid-js/mermaid-cli")
        self.assertIn("PANDOC_SHA256", combined)
        self.assertIn("KUBECONFORM_SHA256", combined)
        self.assertIn("ACTIONLINT_SHA256", combined)
        self.assertRegex(link_text, r"dkhamsing/awesome_bot@sha256:[0-9a-f]{64}")

    def test_mermaid_is_exact_and_lockfile_backed(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        version = package["devDependencies"]["@mermaid-js/mermaid-cli"]

        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertTrue((ROOT / "package-lock.json").is_file())
        ignored = {
            line.strip()
            for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertNotIn("package-lock.json", ignored)
        self.assertTrue(all("npm ci" in path.read_text(encoding="utf-8") for path in self.workflows() if path.name != "check-link.yml" and path.name != "dependabot-automerge.yml"))

    def test_artifacts_are_smoke_tested_and_html_failures_are_not_silent(self):
        verifier = ROOT / "tools" / "verify_artifacts.py"
        self.assertTrue(verifier.is_file())
        for name in ("auto-release.yml", "ci.yaml", "preview-pdf.yml"):
            text = (WORKFLOW_DIR / name).read_text(encoding="utf-8")
            self.assertIn("tools/verify_artifacts.py", text, name)
            self.assertIn("SHA256SUMS", text, name)
        auto_release = (WORKFLOW_DIR / "auto-release.yml").read_text(encoding="utf-8")
        self.assertNotIn("continue-on-error: true", auto_release)

    def test_tagged_release_attests_every_formal_artifact_with_minimum_permissions(self):
        release = (WORKFLOW_DIR / "auto-release.yml").read_text(encoding="utf-8")
        preview = (WORKFLOW_DIR / "preview-pdf.yml").read_text(encoding="utf-8")
        build_part, release_job = release.split("\n  release:\n", 1)

        self.assertIn("contents: write", release_job)
        self.assertIn("id-token: write", release_job)
        self.assertIn("attestations: write", release_job)
        self.assertIn(
            "actions/attest-build-provenance@0f67c3f4856b2e3261c31976d6725780e5e4c373 # v4.1.1",
            release_job,
        )
        self.assertIn("subject-path: |", release_job)
        self.assertIn("dist/docker_practice-*.pdf", release_job)
        self.assertIn("dist/docker_practice-*.html", release_job)
        self.assertIn("dist/SHA256SUMS", release_job)
        self.assertNotIn("attest-build-provenance", build_part)
        self.assertNotIn("attestations: write", build_part)
        self.assertNotIn("id-token: write", build_part)
        self.assertNotIn("attest-build-provenance", preview)
        self.assertIn("mutable preview", preview.lower())
        self.assertIn("tagged release", preview.lower())


if __name__ == "__main__":
    unittest.main()
