"""Run Python tests and enforce function execution for the workbook generator."""

import ast
import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT_DIR / "scripts" / "generar_excel_evaluacion.py",
    ROOT_DIR / "scripts" / "generate_docs.py",
]
TARGET_KEYS = {str(path.resolve()): path.relative_to(ROOT_DIR).as_posix() for path in TARGETS}
CALLED_FUNCTIONS = set()


def record_production_calls(frame, event, _arg):
    if event != "call":
        return
    source = frame.f_code.co_filename
    if source in TARGET_KEYS:
        CALLED_FUNCTIONS.add(f"{TARGET_KEYS[source]}:{frame.f_code.co_name}")


def get_production_functions():
    functions = []
    for path in TARGETS:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        relative_path = path.relative_to(ROOT_DIR).as_posix()
        functions.extend(
            f"{relative_path}:{node.name}"
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
    return sorted(functions)


def run_python_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT_DIR / "tests"), pattern="test_*.py", top_level_dir=str(ROOT_DIR))
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


def write_coverage_report(functions, missing):
    output_dir = ROOT_DIR / "coverage"
    output_dir.mkdir(exist_ok=True)
    report = {
        "scope": [path.relative_to(ROOT_DIR).as_posix() for path in TARGETS],
        "function_coverage_percent": round(100 * (len(functions) - len(missing)) / len(functions), 2),
        "functions": functions,
        "executed_functions": sorted(set(functions) - set(missing)),
        "missing_functions": missing,
    }
    (output_dir / "python-function-coverage.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    functions = get_production_functions()
    sys.path.insert(0, str(ROOT_DIR))
    sys.setprofile(record_production_calls)
    try:
        tests_passed = run_python_tests()
    finally:
        sys.setprofile(None)

    missing = sorted(set(functions) - CALLED_FUNCTIONS)
    write_coverage_report(functions, missing)
    if not tests_passed or missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
