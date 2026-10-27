"""Braced blocks: inner lines one level deeper, edges marked."""

from plantuml_fmt.formatter.blocks import indent_block, mark_block_edges
from tests.unit.plantuml_fmt.formatter._tree import first

__covers__ = (indent_block, mark_block_edges)

SRC = b"@startuml\nnamespace n {\nclass A\nclass B\n}\n@enduml\n"


class TestIndentBlock:
    def test_the_body_gains_a_level_and_the_brace_keeps_the_parent(self) -> None:
        depth = [0] * 7
        indent_block(first(SRC, "namespace_block"), depth)
        assert depth == [0, 0, 1, 1, 0, 0, 0]


class TestMarkBlockEdges:
    def test_marks_the_opening_and_the_closing_rows(self) -> None:
        openers, closers = set(), set()
        mark_block_edges(first(SRC, "namespace_block"), openers, closers)
        assert openers == {1} and closers == {4}
