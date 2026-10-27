"""Opaque bodies freeze: notes, raw blocks, block comments, ref bodies."""

from plantuml_fmt.formatter.opaque import freeze_opaque, freeze_reference_body
from tests.unit.plantuml_fmt.formatter._tree import first

__covers__ = (freeze_opaque, freeze_reference_body)


class TestFreezeOpaque:
    def test_freezes_a_note_body_not_its_edges(self) -> None:
        src = b"@startuml\nnote as N\n  free text\nend note\n@enduml\n"
        frozen = [False] * 6
        freeze_opaque(first(src, "note_statement"), "note_statement", frozen)
        assert frozen == [False, False, True, False, False, False]

    def test_freezes_block_comment_continuations(self) -> None:
        src = b"@startuml\n/' one\n   two\n   three '/\n@enduml\n"
        frozen = [False] * 6
        freeze_opaque(first(src, "block_comment"), "block_comment", frozen)
        assert frozen == [False, False, True, True, False, False]

    def test_leaves_other_kinds_alone(self) -> None:
        frozen = [False] * 3
        freeze_opaque(
            first(b"@startuml\nclass A\n@enduml\n", "class_declaration"),
            "class_declaration",
            frozen,
        )
        assert frozen == [False, False, False]


class TestFreezeReferenceBody:
    def test_freezes_the_body_between_ref_and_end_ref(self) -> None:
        src = b"@startuml\nref over A\n  free text\nend ref\n@enduml\n"
        frozen = [False] * 6
        freeze_reference_body(first(src, "reference"), "end ref", frozen)
        assert frozen == [False, False, True, False, False, False]
