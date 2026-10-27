"""Row helpers shared by every layer of the pass: where a block's closing
child sits, and which rows are frozen as opaque."""

from tree_sitter import Node


def freeze(frozen: list[bool], first_row: int, last_row: int) -> None:
    for row in range(max(first_row, 0), min(last_row + 1, len(frozen))):
        frozen[row] = True


def child_row(node: Node, child_type: str) -> int | None:
    """Row of the last child of the given type, or None."""
    row = None
    for child in node.children:
        if child.type == child_type:
            row = child.start_point[0]
    return row
