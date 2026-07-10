import os
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

    def test_github_actions_fixture_installs_integrity_pinned_validators(self):
        text = FIXTURES["github-actions"].read_text(encoding="utf-8")

        self.assertIn("KUBECONFORM_SHA256", text)
        self.assertIn("ACTIONLINT_SHA256", text)
        self.assertGreaterEqual(text.count("sha256sum -c -"), 2)
        self.assertIn("tools/test_examples.py --require-tools", text)

    def test_local_run_reports_skips_when_tools_are_unavailable(self):
        result = self.run_runner(path="/usr/bin:/bin")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("SKIP"), 4, result.stdout)
        self.assertIn("docker compose", result.stdout)
        self.assertIn("docker buildx", result.stdout)
        self.assertIn("kubeconform", result.stdout)
        self.assertIn("actionlint", result.stdout)

    def test_required_run_fails_when_tools_are_unavailable(self):
        result = self.run_runner("--require-tools", path="/usr/bin:/bin")

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
            self.assertIn("actionlint", commands)


if __name__ == "__main__":
    unittest.main()
