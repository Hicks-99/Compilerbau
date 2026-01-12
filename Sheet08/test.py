from gen.MiniCParser import MiniCParser
from gen.MiniCLexer import MiniCLexer
import sys
from pathlib import Path
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener


class MyErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"{line}:{column} {msg}")


def run_suite(path):
    print(f"\nTesting {path.name}:")
    valid = 0
    files = sorted(path.glob("*.cpp"))
    for f in files:
        parser = MiniCParser(CommonTokenStream(
            MiniCLexer(FileStream(str(f), encoding="utf-8"))))
        errs = MyErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(errs)
        parser.program()

        status = "PASS" if not errs.errors else "FAIL"
        print(f"  [{status}] {f.name}")
        for e in errs.errors[:3]:
            print(f"    {e}")
        if not errs.errors:
            valid += 1
    return valid, len(files)


if __name__ == "__main__":
    base = Path(__file__).parent / "tests"
    p_v, p_t = run_suite(base / "positive")
    n_v, n_t = run_suite(base / "negative")
    print(f"\nSummary: Positive {p_v}/{p_t}, Negative {n_v}/{n_t}")
