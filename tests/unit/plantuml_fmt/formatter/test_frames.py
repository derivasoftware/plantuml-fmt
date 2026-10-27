"""Keyword-closed frames: bodies deeper, clause heads and closer at depth."""

from plantuml_fmt.formatter.frames import KEYWORD_BLOCKS, indent_frame, mark_frame_edges
from tests.unit.plantuml_fmt.formatter._tree import first

__covers__ = (indent_frame, mark_frame_edges)

SRC = b"@startuml\nalt ok\nA -> B\nelse no\nB -> A\nend\n@enduml\n"


class TestIndentFrame:
    def test_bodies_gain_a_level_and_the_else_head_stays(self) -> None:
        closer, clauses = KEYWORD_BLOCKS["frame_block"]
        depth = [0] * 8
        indent_frame(first(SRC, "frame_block"), depth, closer, clauses)
        assert depth == [0, 0, 1, 0, 1, 0, 0, 0]


class TestMarkFrameEdges:
    def test_the_else_row_is_both_an_opener_and_a_closer(self) -> None:
        closer, clauses = KEYWORD_BLOCKS["frame_block"]
        openers, closers = set(), set()
        mark_frame_edges(first(SRC, "frame_block"), openers, closers, closer, clauses)
        assert openers == {1, 3} and closers == {3, 5}
