"""Braced blocks over a real tree: every inner line one level deeper per
enclosing block, the closing braces at the parent's depth, the edges marked."""

from plantuml_fmt.formatter.blocks import BLOCKS, indent_block, mark_block_edges
from tests.integration._grammar import parse

SRC = b"@startuml\nnamespace n {\nclass A {\n+x : int\n}\nclass B\n}\n@enduml\n"


def _blocks(node):
    if node.type in BLOCKS:
        yield node
    for child in node.children:
        yield from _blocks(child)


def test_nested_blocks_indent_one_level_each():
    depth = [0] * len(SRC.split(b"\n"))
    for block in _blocks(parse(SRC).root_node):
        indent_block(block, depth)
    # namespace n {, class A {, +x, }, class B, }
    assert depth[1:7] == [0, 1, 2, 1, 1, 0]


def test_each_block_marks_its_opening_and_closing_rows():
    openers, closers = set(), set()
    for block in _blocks(parse(SRC).root_node):
        mark_block_edges(block, openers, closers)
    assert {1, 2} <= openers and {4, 6} <= closers
