from html.parser import HTMLParser
from pathlib import Path
import unittest


class HTMLSyntaxChecker(HTMLParser):
    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.VOID_ELEMENTS:
            self.stack.append((tag.lower(), self.getpos()))

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in self.VOID_ELEMENTS:
            return

        if not self.stack:
            self.errors.append(f"Etiqueta de cierre inesperada </{tag}> en línea {self.getpos()[0]}")
            return

        last_tag, pos = self.stack.pop()
        if last_tag != tag_lower:
            self.errors.append(
                f"Etiqueta desbalanceada: esperaba </{last_tag}> (abierta en línea {pos[0]}), "
                f"pero encontró </{tag_lower}> en línea {self.getpos()[0]}"
            )


class HTMLSyntaxTests(unittest.TestCase):
    def test_frontend_index_html_syntax(self):
        html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
        content = html_path.read_text(encoding="utf-8")
        checker = HTMLSyntaxChecker()
        checker.feed(content)

        if checker.stack:
            unclosed = [f"<{tag}> abierta en línea {pos[0]}" for tag, pos in checker.stack]
            self.fail(f"Etiquetas sin cerrar: {', '.join(unclosed)}")

        if checker.errors:
            self.fail(f"Errores de sintaxis HTML: {'; '.join(checker.errors)}")


if __name__ == "__main__":
    unittest.main()
