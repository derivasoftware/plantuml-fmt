"""System pass (REQ-00003-4): the two invariants over a real diagram tree.

Every .puml under the corpus roots must format lossless (non-whitespace
bytes preserved in order) and idempotent (a second pass changes nothing).
The default corpus is this repository's own design tree; point
PLANTUML_FMT_CORPUS at any directory (path-separator separated) to run
the same pass over a wild corpus. Marked ``system``: the CI runs it as a
separate coverage pass (``pytest -m system``), so system-test coverage
reports apart from the unit suite's.
"""

import os
import pathlib

import pytest

from plantuml_fmt.formatter import format_bytes

SKIP_DIRS = {"node_modules", ".venv", ".git", "build"}
_DEFAULT = str(pathlib.Path(__file__).resolve().parents[2] / "design")


def _corpus() -> list[pathlib.Path]:
    roots = os.environ.get("PLANTUML_FMT_CORPUS", _DEFAULT).split(os.pathsep)
    return sorted(
        path
        for root in roots
        for path in pathlib.Path(root).rglob("*.puml")
        if not SKIP_DIRS & set(path.parts)
    )


def _non_ws(data: bytes) -> bytes:
    return b"".join(data.split())


@pytest.mark.system
@pytest.mark.parametrize("path", _corpus(), ids=lambda p: p.name)
def test_corpus_file_formats_lossless_and_idempotent(path: pathlib.Path) -> None:
    src = path.read_bytes()
    once = format_bytes(src)
    assert _non_ws(once) == _non_ws(src), f"lossy: {path}"
    assert format_bytes(once) == once, f"unstable: {path}"
