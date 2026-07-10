import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tools" / "verify_artifacts.py"


class VerifyArtifactsTests(unittest.TestCase):
    def run_verifier(self, *args):
        return subprocess.run(
            [sys.executable, str(VERIFIER), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_verifies_html_title_and_writes_sha256_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "reader.html"
            checksums = Path(tmp) / "SHA256SUMS"
            artifact.write_text(
                "<!doctype html><html><head><title>Docker —— 从入门到实践</title></head></html>",
                encoding="utf-8",
            )

            result = self.run_verifier(
                "--title",
                "Docker —— 从入门到实践",
                "--html",
                str(artifact),
                "--checksums",
                str(checksums),
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            expected = hashlib.sha256(artifact.read_bytes()).hexdigest()
            self.assertEqual(checksums.read_text(encoding="utf-8"), f"{expected}  reader.html\n")

    def test_rejects_missing_artifact(self):
        result = self.run_verifier(
            "--title",
            "Docker —— 从入门到实践",
            "--html",
            "/does/not/exist.html",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr)

    def test_rejects_wrong_html_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "reader.html"
            artifact.write_text("<title>Wrong book</title>", encoding="utf-8")

            result = self.run_verifier(
                "--title",
                "Docker —— 从入门到实践",
                "--html",
                str(artifact),
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("title mismatch", result.stderr)

    def test_accepts_mdpress_site_title_with_page_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp) / "_site"
            site.mkdir()
            (site / "index.html").write_text(
                "<title>Docker 从入门到实践 - Docker 从入门到实践</title>",
                encoding="utf-8",
            )

            result = self.run_verifier(
                "--title",
                "Docker 从入门到实践",
                "--site",
                str(site),
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
