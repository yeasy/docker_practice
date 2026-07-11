import hashlib
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "test_examples.py"
FIXTURES = {
    "compose": ROOT / "examples" / "validated" / "compose" / "compose.yaml",
    "dockerfile": ROOT / "examples" / "validated" / "dockerfile" / "Dockerfile",
    "kubernetes": ROOT / "examples" / "validated" / "kubernetes" / "web.yaml",
    "github-actions": ROOT / "examples" / "validated" / "github-actions" / "validate.yml",
}
CHAPTER_SNIPPETS = {
    "compose": ROOT / "11_compose" / "11.5_compose_file.md",
    "dockerfile": ROOT / "07_dockerfile" / "README.md",
    "kubernetes": ROOT / "13_kubernetes_concepts" / "13.5_practice.md",
    "github-actions": ROOT / "21_case_devops" / "21.2_github_actions.md",
}
SCHEMA_ROOT = (
    ROOT
    / "examples"
    / "validated"
    / "kubernetes"
    / "schemas"
    / "v1.31.0-standalone-strict"
)


class ExampleValidationTests(unittest.TestCase):
    def run_runner(self, *args, path=None, env=None):
        run_env = os.environ.copy()
        run_env.update(env or {})
        if path is not None:
            run_env["PATH"] = path
        return subprocess.run(
            [sys.executable, str(RUNNER), *args],
            cwd=ROOT,
            env=run_env,
            capture_output=True,
            text=True,
        )

    def test_canonical_fixture_files_exist(self):
        missing = [name for name, path in FIXTURES.items() if not path.is_file()]

        self.assertEqual(missing, [])

    def test_relevant_chapters_link_to_canonical_fixtures(self):
        references = {
            ROOT / "11_compose" / "11.5_compose_file.md": "../examples/validated/compose/compose.yaml",
            ROOT / "07_dockerfile" / "README.md": "../examples/validated/dockerfile/Dockerfile",
            ROOT / "13_kubernetes_concepts" / "13.5_practice.md": "../examples/validated/kubernetes/web.yaml",
            ROOT / "21_case_devops" / "21.2_github_actions.md": "../examples/validated/github-actions/validate.yml",
        }

        missing = []
        for chapter, fixture in references.items():
            if fixture not in chapter.read_text(encoding="utf-8"):
                missing.append(f"{chapter.relative_to(ROOT)} -> {fixture}")
        self.assertEqual(missing, [])

    def test_chapter_canonical_blocks_exactly_match_fixtures(self):
        mismatches = []
        for name, chapter in CHAPTER_SNIPPETS.items():
            text = chapter.read_text(encoding="utf-8")
            match = re.search(
                rf"<!-- canonical-example: {re.escape(name)} -->\s*```[^\n]*\n(.*?)\n```",
                text,
                re.DOTALL,
            )
            expected = FIXTURES[name].read_text(encoding="utf-8").strip()
            actual = match.group(1).strip() if match else None
            if actual != expected:
                mismatches.append(name)
        self.assertEqual(mismatches, [])
        self.assertNotIn(
            "type: NodePort",
            CHAPTER_SNIPPETS["kubernetes"].read_text(encoding="utf-8"),
        )

    def test_kubernetes_fixture_has_vendored_schema_provenance(self):
        provenance = SCHEMA_ROOT.parent / "README.md"
        schema_files = (
            SCHEMA_ROOT / "deployment-apps-v1.json",
            SCHEMA_ROOT / "service-v1.json",
        )

        self.assertTrue(provenance.is_file())
        provenance_text = provenance.read_text(encoding="utf-8")
        self.assertIn("v1.31.0-standalone-strict", provenance_text)
        self.assertRegex(provenance_text, r"upstream commit: `[0-9a-f]{40}`")
        for schema in schema_files:
            self.assertTrue(schema.is_file(), schema)
            digest = hashlib.sha256(schema.read_bytes()).hexdigest()
            self.assertIn(f"`{schema.name}`: `{digest}`", provenance_text)

    def test_dockerfile_fixture_has_no_remote_base_image(self):
        dockerfile = FIXTURES["dockerfile"].read_text(encoding="utf-8")

        self.assertEqual(dockerfile.splitlines()[0], "FROM scratch")

    def test_github_actions_fixture_installs_integrity_pinned_validators(self):
        text = FIXTURES["github-actions"].read_text(encoding="utf-8")

        self.assertIn("KUBECONFORM_SHA256", text)
        self.assertIn("ACTIONLINT_SHA256", text)
        self.assertGreaterEqual(text.count("sha256sum -c -"), 2)
        self.assertIn("tools/test_examples.py --require-tools", text)

    def test_local_run_reports_skips_when_tools_are_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_runner(path=tmp)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("SKIP"), 4, result.stdout)
        self.assertIn("docker compose", result.stdout)
        self.assertIn("docker buildx", result.stdout)
        self.assertIn("kubeconform", result.stdout)
        self.assertIn("actionlint", result.stdout)

    def test_required_run_fails_when_tools_are_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_runner("--require-tools", path=tmp)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout.count("UNAVAILABLE"), 4, result.stdout)

    def test_available_tools_receive_the_canonical_validation_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            log = tmp_path / "commands.log"
            shim = tmp_path / "validator-shim"
            shim.write_text(
                "#!/bin/sh\n"
                "printf '%s %s\\n' \"$(basename \"$0\")\" \"$*\" >> \"$COMMAND_LOG\"\n"
                "exit 0\n",
                encoding="utf-8",
            )
            shim.chmod(0o755)
            for name in ("docker", "kubeconform", "actionlint"):
                (tmp_path / name).symlink_to(shim)

            result = self.run_runner(
                "--require-tools",
                path=f"{tmp_path}:/usr/bin:/bin",
                env={"COMMAND_LOG": str(log)},
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            commands = log.read_text(encoding="utf-8")
            self.assertIn("docker compose version", commands)
            self.assertIn("docker compose -f", commands)
            self.assertIn("config --quiet", commands)
            self.assertIn("docker buildx version", commands)
            self.assertIn("docker buildx build --check", commands)
            self.assertIn("kubeconform -strict -summary", commands)
            self.assertIn("-schema-location file://", commands)
            self.assertIn("actionlint", commands)

    def test_runner_uses_only_vendored_schema_when_network_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            success = tmp_path / "success"
            success.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            success.chmod(0o755)
            for name in ("docker", "actionlint"):
                (tmp_path / name).symlink_to(success)

            kubeconform = tmp_path / "kubeconform"
            kubeconform.write_text(
                "#!/bin/sh\n"
                "case \"$*\" in\n"
                "  *'-schema-location file://'*) exit 0 ;;\n"
                "  *) exit 23 ;;\n"
                "esac\n",
                encoding="utf-8",
            )
            kubeconform.chmod(0o755)

            result = self.run_runner(
                "--require-tools",
                path=f"{tmp_path}:/usr/bin:/bin",
                env={
                    "HTTP_PROXY": "http://127.0.0.1:9",
                    "HTTPS_PROXY": "http://127.0.0.1:9",
                    "NO_PROXY": "",
                },
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
