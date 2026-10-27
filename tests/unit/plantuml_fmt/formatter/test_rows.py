"""Row helpers: freezing a range and finding a closing child's row."""

from plantuml_fmt.formatter.rows import child_row, freeze
from tests.unit.plantuml_fmt.formatter._tree import first

__covers__ = (freeze, child_row)


class TestFreeze:
    def test_freezes_the_inclusive_range(self) -> None:
        frozen = [False] * 5
        freeze(frozen, 1, 3)
        assert frozen == [False, True, True, True, False]

    def test_clips_to_the_document(self) -> None:
        frozen = [False] * 3
        freeze(frozen, -2, 9)
        assert frozen == [True, True, True]


class TestChildRow:
    def test_finds_the_closing_brace_row(self) -> None:
        node = first(b"@startuml\nclass A {\n+x : int\n}\n@enduml\n", "entity_body")
        assert child_row(node, "}") == 3

    def test_is_none_when_the_child_is_absent(self) -> None:
        node = first(b"@startuml\nclass A {\n+x : int\n}\n@enduml\n", "entity_body")
        assert child_row(node, "end note") is None
