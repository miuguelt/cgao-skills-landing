import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from scripts import generate_docs


class GeneratedDocumentTests(unittest.TestCase):
    def test_all_published_pdf_sources_generate_and_the_rubric_stays_on_one_page(self):
        original_output_dir = generate_docs.OUTPUT_DIR
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_dir = Path(temporary_directory)
            generate_docs.OUTPUT_DIR = str(output_dir)
            try:
                generate_docs.generate_checklist()
                generate_docs.generate_guide()
                generate_docs.generate_rubric()
                manual_path = output_dir / "Manual_Sostenibilidad_y_Etica.pdf"
                generate_docs.create_sustainability_manual(
                    str(manual_path), "Manual de Sostenibilidad y Código de Ética"
                )

                expected_names = [
                    "Checklist_Jueces_Dia0.pdf",
                    "Guia_Tecnica_Diseno_Prueba.pdf",
                    "Rubrica_Maestra_Template.pdf",
                    "Manual_Sostenibilidad_y_Etica.pdf",
                ]
                for name in expected_names:
                    self.assertTrue((output_dir / name).is_file(), name)
                    self.assertGreater((output_dir / name).stat().st_size, 1000, name)

                rubric = PdfReader(str(output_dir / "Rubrica_Maestra_Template.pdf"))
                self.assertEqual(len(rubric.pages), 1)
                rubric_text = " ".join(page.extract_text() or "" for page in rubric.pages).casefold()
                for required in ("ejemplo adso", "m-j-p", "69 pts", "23 pts", "8 pts", "m7", "p2"):
                    self.assertIn(required, rubric_text)

                manual = PdfReader(str(manual_path))
                manual_text = " ".join(page.extract_text() or "" for page in manual.pages).casefold()
                for required in ("blanco", "verde", "negro", "resolución 2184"):
                    self.assertIn(required, manual_text)
            finally:
                generate_docs.OUTPUT_DIR = original_output_dir


if __name__ == "__main__":
    unittest.main()
