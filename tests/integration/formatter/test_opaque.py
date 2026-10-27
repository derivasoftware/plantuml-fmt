"""Opaque bodies over a real tree: the rows of a note body, a raw block body,
block-comment continuations and a ref body are frozen; their edges are not."""

from plantuml_fmt.formatter.frames import KEYWORD_BLOCKS
from plantuml_fmt.formatter.opaque import freeze_opaque, freeze_reference_body
from plantuml_fmt.rules import get_parser


def _frozen(src: bytes) -> list[int]:
    frozen = [False] * len(src.split(b"\n"))
    stack = [get_parser().parse(src).root_node]
    while stack:
        node = stack.pop()
        if node.type == "reference":
            freeze_reference_body(node, KEYWORD_BLOCKS["reference"][0], frozen)
        else:
            freeze_opaque(node, node.type, frozen)
        stack.extend(node.children)
    return [row for row, cold in enumerate(frozen) if cold]


def test_a_note_body_is_frozen_between_its_edges():
    src = b"@startuml\nnote right of A\n  keep   this\n   exact\nend note\n@enduml\n"
    assert _frozen(src) == [2, 3]


def test_block_comment_continuations_are_frozen():
    src = b"@startuml\n/' one\n     two\n   three '/\nclass A\n@enduml\n"
    assert _frozen(src) == [2, 3]


def test_a_ref_body_is_frozen():
    src = b"@startuml\nref over A, B\n  free   text\nend ref\n@enduml\n"
    assert _frozen(src) == [2]


def test_ordinary_statements_are_not():
    assert _frozen(b"@startuml\nclass A\nA --> B\n@enduml\n") == []
