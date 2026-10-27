"""Reading the tree: the grammar instance is built once; a node's bytes and
its one-line test."""

from plantuml_fmt.rules.reading import get_parser, single_line, text
from tests.unit.plantuml_fmt.rules._tree import first

__covers__ = (get_parser, text, single_line)


class TestGetParser:
    def test_is_built_once(self) -> None:
        assert get_parser() is get_parser()


class TestText:
    def test_slices_the_node_out_of_its_source(self) -> None:
        src = b"@startuml\nA --> B : uses\n@enduml\n"
        assert text(src, first(src, "label")) == b"uses"


class TestSingleLine:
    def test_a_trailing_newline_does_not_count_as_a_second_row(self) -> None:
        assert single_line(first(b"@startuml\nA --> B\n@enduml\n", "relation"))

    def test_a_body_over_rows_is_not_one_line(self) -> None:
        assert not single_line(
            first(b"@startuml\nclass A {\n+x\n}\n@enduml\n", "entity_body")
        )
