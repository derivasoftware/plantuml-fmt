"""The pre-commit hook declaration stays wired to the console script."""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_precommit_hook_declared():
    text = (ROOT / ".pre-commit-hooks.yaml").read_text()
    assert "- id: plantuml-fmt" in text
    assert "entry: plantuml-fmt" in text
    assert "language: python" in text
