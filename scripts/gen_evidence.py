#!/usr/bin/env python3
"""Produce the execution evidence the docs read (test-results/).

Two runs: the unit suite via pytest (junit + unit coverage, configured in
pyproject addopts), and the system pass — the wild-corpus invariant eval
over this repository's own design tree, through the real API, under
coverage. The folio regions in README.md and doc/ read these files; run
this before `folio inject --check`.
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run(*cmd: str) -> None:
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> int:
    (ROOT / "test-results").mkdir(exist_ok=True)
    run(sys.executable, "-m", "pytest", "-q")
    st_data = "test-results/.coverage-st"
    run(
        sys.executable, "-m", "coverage", "run",
        f"--data-file={st_data}", "--source=plantuml_fmt",
        "scripts/eval_wild_corpus.py", "design",
    )
    run(
        sys.executable, "-m", "coverage", "xml",
        f"--data-file={st_data}", "-o", "test-results/coverage-st.xml",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
