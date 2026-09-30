import csv
import unittest
from pathlib import Path

from tests.test_challenge_document import read_docx_tables


ROOT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT_DIR / "frontend" / "assets" / "documents"


class SustainabilityContentTests(unittest.TestCase):
    def test_sustainability_criteria_match_across_rubric_manual_and_challenge(self):
        with (DOCS_DIR / "Rubrica_Maestra_Template.csv").open(
            encoding="utf-8-sig", newline=""
        ) as source:
            criteria = {row["ID"]: row for row in csv.DictReader(source)}

        self.assertIn("programas que ya no necesita", criteria["M7"]["CRITERIO_DETALLADO"].casefold())
        self.assertIn("archivos temporales", criteria["M7"]["CRITERIO_DETALLADO"].casefold())
        waste_rule = criteria["P2"]["CRITERIO_DETALLADO"].casefold()
        for color in ("blanco", "verde", "negro"):
            self.assertIn(color, waste_rule)
        self.assertIn("limpios y secos", waste_rule)
        self.assertIn("orgánicos aprovechables", waste_rule)

        markdown = (DOCS_DIR / "Rubrica_Maestra_Template.md").read_text(encoding="utf-8").casefold()
        manual = (DOCS_DIR / "Manual_Sostenibilidad_y_Etica.md").read_text(encoding="utf-8").casefold()
        self.assertIn("69", markdown)
        self.assertIn("23", markdown)
        self.assertIn("8", markdown)
        self.assertIn("resolución 2184 de 2019", manual)
        for color in ("blanco", "verde", "negro"):
            self.assertIn(color, markdown)
            self.assertIn(color, manual)

        _, challenge_text = read_docx_tables(
            DOCS_DIR / "Reto_ejemplo_aprendiz_ADSO_CGAO_Skills.docx"
        )
        challenge_text = challenge_text.casefold()
        for phrase in ("archivos temporales", "blanco", "verde", "negro"):
            self.assertIn(phrase, challenge_text)


if __name__ == "__main__":
    unittest.main()
