import csv
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


ROOT_DIR = Path(__file__).resolve().parents[1]
WORD_PATH = ROOT_DIR / "frontend" / "assets" / "documents" / "Reto_ejemplo_aprendiz_ADSO_CGAO_Skills.docx"
RUBRIC_PATH = ROOT_DIR / "frontend" / "assets" / "documents" / "Rubrica_Maestra_Template.csv"
WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def read_docx_tables(path):
    with ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
    tables = []
    for table in document.findall(f".//{WORD_NS}tbl"):
        rows = []
        for row in table.findall(f"{WORD_NS}tr"):
            cells = []
            for cell in row.findall(f"{WORD_NS}tc"):
                text = "".join(node.text or "" for node in cell.findall(f".//{WORD_NS}t"))
                cells.append(text)
            rows.append(cells)
        tables.append(rows)
    paragraphs = " ".join(
        node.text or ""
        for node in document.findall(f".//{WORD_NS}p//{WORD_NS}t")
    )
    return tables, paragraphs


class ChallengeDocumentTests(unittest.TestCase):
    def test_challenge_rubric_matches_master_ids_modules_types_and_points(self):
        tables, _ = read_docx_tables(WORD_PATH)
        challenge_rubric = tables[-1]
        self.assertEqual(challenge_rubric[0], ["ID", "Módulo", "Criterio", "Tipo", "Puntos"])

        with RUBRIC_PATH.open(encoding="utf-8-sig", newline="") as source:
            master_rows = list(csv.DictReader(source))

        word_rows = challenge_rubric[1:]
        self.assertEqual(len(word_rows), 12)
        self.assertEqual(
            [(row[0], row[1], row[2], row[3], float(row[4])) for row in word_rows],
            [
                (row["ID"], row["MODULO"], row["ASPECTO"], row["TIPO_(M/J/P)"], float(row["PUNTOS_MAX"]))
                for row in master_rows
            ],
        )

    def test_challenge_explains_judgment_conversion_and_local_storage(self):
        _, text = read_docx_tables(WORD_PATH)
        normalized = text.casefold()
        self.assertIn("almacenamiento local", normalized)
        self.assertIn("0 o el puntaje máximo", normalized)
        self.assertIn("nivel de 0 a 3", normalized)
        self.assertIn("100 puntos", normalized)

    def test_challenge_covers_rubric_boundaries_and_module_d_actions(self):
        tables, paragraphs = read_docx_tables(WORD_PATH)
        cases = " ".join(" ".join(row) for row in tables[1]).casefold()
        normalized = paragraphs.casefold()

        for evidence in (
            "de 2 y 40 caracteres", "40 caracteres", "1 y 100", "decimal", "101",
            "alias vacío", "41 caracteres", "no se crea",
        ):
            self.assertIn(evidence, cases)
        self.assertIn("apaga el monitor o el equipo", normalized)
        self.assertIn("recipiente rotulado", normalized)
        self.assertIn("blanco para aprovechables limpios y secos", normalized)
        self.assertIn("verde para orgánicos aprovechables", normalized)
        self.assertIn("negro para no aprovechables", normalized)
        self.assertIn("resolución 2184 de 2019", normalized)

    def test_published_word_copies_match_each_other(self):
        self.assertTrue(WORD_PATH.exists(), f"Debe existir el documento {WORD_PATH}")
        self.assertGreater(WORD_PATH.stat().st_size, 1000, "El documento Word debe tener contenido")
        artifacts_copy = ROOT_DIR / "artifacts" / WORD_PATH.name
        if artifacts_copy.exists():
            self.assertEqual(artifacts_copy.read_bytes(), WORD_PATH.read_bytes(), "La copia en artifacts debe estar sincronizada")


if __name__ == "__main__":
    unittest.main()
