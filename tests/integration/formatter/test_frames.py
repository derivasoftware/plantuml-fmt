"""Sequence frames and activity control flow over a real tree: bodies one
level deeper, clause heads and closers at the frame's depth."""

from plantuml_fmt.formatter.frames import KEYWORD_BLOCKS, indent_frame, mark_frame_edges
from plantuml_fmt.rules import get_parser


def _frame_depths(src: bytes) -> list[int]:
    depth = [0] * len(src.split(b"\n"))
    stack = [get_parser().parse(src).root_node]
    while stack:
        node = stack.pop()
        if node.type in KEYWORD_BLOCKS:
            closer, clauses = KEYWORD_BLOCKS[node.type]
            indent_frame(node, depth, closer, clauses)
        stack.extend(node.children)
    return depth


def test_a_loop_body_gains_a_level():
    src = b"@startuml\nloop each\ncli -> repo\nend\n@enduml\n"
    assert _frame_depths(src)[1:4] == [0, 1, 0]


def test_an_alt_else_head_stays_at_frame_depth():
    src = b"@startuml\nalt ok\nA -> B\nelse no\nB -> A\nend\n@enduml\n"
    assert _frame_depths(src)[1:6] == [0, 1, 0, 1, 0]


def test_an_if_chain_indents_its_branches():
    src = b"@startuml\nstart\nif (a?) then (yes)\n:x;\nelse (no)\n:y;\nendif\nstop\n@enduml\n"
    assert _frame_depths(src)[2:7] == [0, 1, 0, 1, 0]


def test_else_rows_are_both_edges():
    src = b"@startuml\nalt ok\nA -> B\nelse no\nB -> A\nend\n@enduml\n"
    openers, closers = set(), set()
    stack = [get_parser().parse(src).root_node]
    while stack:
        node = stack.pop()
        if node.type in KEYWORD_BLOCKS:
            closer, clauses = KEYWORD_BLOCKS[node.type]
            mark_frame_edges(node, openers, closers, closer, clauses)
        stack.extend(node.children)
    assert 3 in openers and 3 in closers and 5 in closers
