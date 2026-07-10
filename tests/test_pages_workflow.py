import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"
FULL_ACTION_SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")


class PagesWorkflowTests(unittest.TestCase):
    def workflow_text(self):
        self.assertTrue(WORKFLOW.is_file(), "custom Pages workflow is missing")
        return WORKFLOW.read_text(encoding="utf-8")

    def test_custom_pages_workflow_exists(self):
        self.assertTrue(WORKFLOW.is_file(), "custom Pages workflow is missing")

    def test_builds_mdpress_site_without_jekyll(self):
        text = self.workflow_text()

        self.assertIn("npm run build", text)
        self.assertIn("MDPRESS_SHA256", text)
        self.assertIn('install -m 0755 "$RUNNER_TEMP/mdpress" "$RUNNER_TEMP/bin/mdpress"', text)
        self.assertIn('echo "$RUNNER_TEMP/bin" >> "$GITHUB_PATH"', text)
        self.assertRegex(text, r"path:\s*_site\b")
        self.assertNotIn("jekyll", text.lower())

    def test_build_and_deploy_jobs_have_minimum_permissions(self):
        text = self.workflow_text()

        self.assertRegex(
            text,
            r"(?ms)^  build:\n    permissions:\n      contents: read\n      pages: read\b",
        )
        self.assertRegex(
            text,
            r"(?ms)^  deploy:.*?permissions:\n      pages: write\n      id-token: write\b",
        )
        self.assertRegex(text, r"(?ms)^  deploy:.*?needs: build\b")
        self.assertIn("environment:", text)
        self.assertIn("name: github-pages", text)

    def test_actions_are_immutable_and_checkout_drops_credentials(self):
        text = self.workflow_text()
        actions = re.findall(r"\buses:\s*([^\s#]+)", text)

        self.assertGreater(len(actions), 0)
        self.assertTrue(all(FULL_ACTION_SHA.fullmatch(action) for action in actions), actions)
        self.assertRegex(text, r"actions/checkout@[0-9a-f]{40}\s+# v\d")
        self.assertRegex(
            text,
            r"(?ms)actions/checkout@[0-9a-f]{40}.*?with:\n\s+persist-credentials: false",
        )

    def test_documents_manual_pages_source_setting(self):
        text = self.workflow_text()

        self.assertIn("Settings > Pages > Source", text)
        self.assertIn("GitHub Actions", text)


if __name__ == "__main__":
    unittest.main()
