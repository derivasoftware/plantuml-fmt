"""The formatter's surface: bytes in, bytes out, whitespace only."""

import pytest

from plantuml_fmt.formatter.format import (
    collect,
    format_bytes,
    format_text,
    rewrite,
    spans_line,
)
from plantuml_fmt.rules import get_parser
from tests.unit.plantuml_fmt.formatter._tree import first as _first

__covers__ = (format_bytes, format_text, collect, rewrite, spans_line)


class TestFormatBytes:
    def test_indents_a_block_body_two_spaces(self) -> None:
        assert (
            format_bytes(b"@startuml\nclass A {\n+x : int\n}\n@enduml\n")
            == b"@startuml\nclass A {\n  + x : int\n}\n@enduml\n"
        )

    def test_collapses_a_run_of_blank_lines_to_one(self) -> None:
        assert (
            format_bytes(b"@startuml\nclass A\n\n\n\nclass B\n@enduml\n")
            == b"@startuml\nclass A\n\nclass B\n@enduml\n"
        )

    def test_keeps_a_note_body_byte_identical(self) -> None:
        src = b"@startuml\nnote as N\n    free   text\nend note\n@enduml\n"
        assert format_bytes(src) == src

    def test_reaches_a_fixed_point_in_one_pass(self) -> None:
        once = format_bytes(
            b"@startuml\nnamespace n {\nclass A {\n+go( a ,b ) : int\n}\n}\nA-->B\n@enduml\n"
        )
        assert format_bytes(once) == once

    def test_rejects_an_unknown_member_style(self) -> None:
        with pytest.raises(ValueError):
            format_bytes(b"@startuml\n@enduml\n", "sideways")


class TestFormatText:
    def test_is_format_bytes_over_text(self) -> None:
        assert (
            format_text("@startuml\nA   -->   B\n@enduml\n")
            == "@startuml\nA --> B\n@enduml\n"
        )

    def test_glued_tokens_stay_glued(self) -> None:
        assert (
            format_text("@startuml\nA-->B\n@enduml\n") == "@startuml\nA-->B\n@enduml\n"
        )


class TestCollect:
    def test_records_depth_rewrites_and_edges_of_a_block(self) -> None:
        src = b"@startuml\nclass A {\n+x : int\n}\nA --> B\n@enduml\n"
        lines = src.split(b"\n")
        depth, frozen = [0] * len(lines), [False] * len(lines)
        rewrites, openers, closers = {}, set(), set()
        collect(
            get_parser().parse(src).root_node, depth, frozen, rewrites, openers, closers
        )
        assert depth[2] == 1 and depth[3] == 0
        assert sorted(rewrites) == [2, 4]
        assert 1 in openers and 3 in closers

    def test_freezes_a_ref_body(self) -> None:
        src = b"@startuml\nref over A\n  free text\nend ref\n@enduml\n"
        lines = src.split(b"\n")
        depth, frozen = [0] * len(lines), [False] * len(lines)
        collect(get_parser().parse(src).root_node, depth, frozen, {}, set(), set())
        assert frozen[2]


class TestRewrite:
    def test_dispatches_a_relation_and_a_member(self) -> None:
        rel_src = b"@startuml\nA   -->   B\n@enduml\n"
        assert rewrite(_first(rel_src, "relation"), rel_src, "preserve") == b"A --> B"
        mem_src = b"@startuml\nclass A {\n+x   :   int\n}\n@enduml\n"
        assert rewrite(_first(mem_src, "member"), mem_src, "preserve") == b"+ x : int"


class TestSpansLine:
    def test_a_relation_alone_on_its_line_spans_it(self) -> None:
        src = b"@startuml\nA --> B\n@enduml\n"
        assert spans_line(_first(src, "relation"), 1, src.split(b"\n")[1])

    def test_a_node_not_at_the_first_non_blank_byte_does_not(self) -> None:
        node = _first(b"@startuml\nA --> B\n@enduml\n", "relation")
        assert not spans_line(node, 1, b"  A --> B")

    def test_a_node_ending_on_its_row_with_bytes_behind_does_not(self) -> None:
        src = b"@startuml\nnamespace o { class A }\n@enduml\n"
        node = _first(src, "class_declaration")
        assert node.end_point[0] == 1
        assert not spans_line(node, 1, src.split(b"\n")[1])
