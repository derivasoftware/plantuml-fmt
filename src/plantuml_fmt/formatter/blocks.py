"""Braced blocks: their inner lines gain one indentation level, and their
opening and closing rows are edges the blank-line policy respects."""

from tree_sitter import Node

from plantuml_fmt.formatter.rows import child_row

BLOCKS = {
    "entity_body",
    "package_block",
    "namespace_block",
    "together_block",
    "partition_block",
}


def indent_block(node: Node, depth: list[int]) -> None:
    # the closing-brace row keeps the parent depth; blocks that consume
    # a trailing newline end on the NEXT row, so anchor on the '}' child
    brace_row = child_row(node, "}")
    if brace_row is None:
        brace_row = node.end_point[0]
    for row in range(node.start_point[0] + 1, brace_row):
        depth[row] += 1


def mark_block_edges(node: Node, openers: set[int], closers: set[int]) -> None:
    openers.add(node.start_point[0])
    brace_row = child_row(node, "}")
    if brace_row is not None:
        closers.add(brace_row)
