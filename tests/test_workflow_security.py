import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
FULL_ACTION_SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")


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


if __name__ == "__main__":
    unittest.main()
