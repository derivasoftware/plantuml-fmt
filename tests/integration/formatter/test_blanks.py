"""The blank-line policy over a document's rows and its block edges."""

from plantuml_fmt.formatter.blanks import keep_blank


def _kept(
    lines: list[bytes], openers: set[int], closers: set[int], frozen=None
) -> list[int]:
    frozen = frozen or [False] * len(lines)
    return [
        row
        for row, line in enumerate(lines)
        if not line.strip()
        and not frozen[row]
        and keep_blank(row, lines, frozen, openers, closers)
    ]


def test_a_run_of_blanks_keeps_only_its_first():
    lines = [b"class A", b"", b"", b"", b"class B"]
    assert _kept(lines, set(), set()) == [1]


def test_blanks_touching_a_block_edge_go():
    lines = [b"namespace n {", b"", b"class A", b"", b"}"]
    assert _kept(lines, {0}, {4}) == []


def test_a_single_blank_between_top_level_statements_stays():
    lines = [b"class A", b"", b"class B"]
    assert _kept(lines, set(), set()) == [1]


def test_frozen_blank_rows_are_never_decided():
    lines = [b"note as N", b"", b"", b"end note"]
    frozen = [False, True, True, False]
    assert _kept(lines, {0}, {3}, frozen) == []
