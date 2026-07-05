import tempfile
import unittest
from base64 import b64encode
from pathlib import Path

from tools.prepare_pdf_sources import normalize_markdown_asset_paths, prepare_pdf_sources


class PreparePdfSourcesTest(unittest.TestCase):
    def test_normalizes_relative_markdown_and_html_image_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            book_dir = Path(tmp)
            (book_dir / "_images").mkdir()
            (book_dir / "_images" / "virtualization.png").write_bytes(b"virtualization")
            (book_dir / "_images" / "docker.png").write_bytes(b"docker")
            text = "\n".join(
                [
                    "![传统虚拟化](../_images/virtualization.png)",
                    "![Remote](https://example.com/image.png)",
                    '<img alt="Docker" src="../_images/docker.png">',
                ]
            )

            normalized, count = normalize_markdown_asset_paths(text, "01_introduction", book_dir)
            virtualization_uri = "data:image/png;base64," + b64encode(b"virtualization").decode("ascii")
            docker_uri = "data:image/png;base64," + b64encode(b"docker").decode("ascii")

            self.assertIn(f"![传统虚拟化]({virtualization_uri})", normalized)
            self.assertIn("![Remote](https://example.com/image.png)", normalized)
            self.assertIn(f'src="{docker_uri}"', normalized)
            self.assertEqual(count, 2)

    def test_prepares_temp_tree_without_mutating_source_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            target = Path(tmp) / "target"
            (source / "01_introduction").mkdir(parents=True)
            (source / "_images").mkdir()
            source_md = source / "01_introduction" / "1.2_what.md"
            source_md.write_text("![Docker](../_images/docker.png)\n", encoding="utf-8")
            (source / "_images" / "docker.png").write_bytes(b"png")

            result = prepare_pdf_sources(source, target)

            self.assertEqual(result.markdown_files, 1)
            self.assertEqual(result.rewritten_paths, 1)
            self.assertEqual(source_md.read_text(encoding="utf-8"), "![Docker](../_images/docker.png)\n")
            self.assertEqual(
                (target / "01_introduction" / "1.2_what.md").read_text(encoding="utf-8"),
                "![Docker](data:image/png;base64,cG5n)\n",
            )
            self.assertEqual((target / "_images" / "docker.png").read_bytes(), b"png")


if __name__ == "__main__":
    unittest.main()
