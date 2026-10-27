"""The blank-line policy: collapse runs, drop blanks at block edges."""

from plantuml_fmt.formatter.blanks import is_soft_blank, keep_blank, neighbor

__covers__ = (is_soft_blank, neighbor, keep_blank)

LINES = [
    b"@startuml",
    b"class A {",
    b"",
    b"+x : int",
    b"",
    b"",
    b"}",
    b"class B",
    b"@enduml",
]
FROZEN = [False] * len(LINES)


class TestIsSoftBlank:
    def test_a_blank_unfrozen_row_is_soft(self) -> None:
        assert is_soft_blank(LINES, FROZEN, 2)

    def test_a_frozen_blank_row_is_not(self) -> None:
        frozen = FROZEN.copy()
        frozen[2] = True
        assert not is_soft_blank(LINES, frozen, 2)


class TestNeighbor:
    def test_skips_soft_blanks_in_both_directions(self) -> None:
        assert neighbor(4, 1, LINES, FROZEN) == 6
        assert neighbor(5, -1, LINES, FROZEN) == 3


class TestKeepBlank:
    def test_drops_a_blank_after_an_opener(self) -> None:
        assert not keep_blank(2, LINES, FROZEN, {1}, {6})

    def test_drops_a_blank_before_a_closer(self) -> None:
        assert not keep_blank(4, LINES, FROZEN, {1}, {6})

    def test_keeps_the_first_blank_of_a_run_between_statements(self) -> None:
        lines = [b"class A", b"", b"", b"class B"]
        frozen = [False] * 4
        assert keep_blank(1, lines, frozen, set(), set())
        assert not keep_blank(2, lines, frozen, set(), set())
