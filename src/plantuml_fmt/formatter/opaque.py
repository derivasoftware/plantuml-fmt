"""Opaque content — note bodies, raw-block bodies, block-comment
continuation lines and ref bodies — is frozen: its rows pass through
byte-identical."""

from tree_sitter import Node

from plantuml_fmt.formatter.rows import child_row, freeze


def freeze_opaque(node: Node, kind: str, frozen: list[bool]) -> None:
    """Freeze the lines whose content is opaque text: a note body, a raw
    block body and the continuation lines of a block comment."""
    if kind == "note_statement":
        end_row = child_row(node, "end note")
        if end_row is not None:
            freeze(frozen, node.start_point[0] + 1, end_row - 1)
    elif kind == "raw_block":
        tail_row = child_row(node, "raw_line")
        if tail_row is not None:
            freeze(frozen, node.start_point[0] + 1, tail_row - 1)
    elif kind == "block_comment":
        # continuation lines live inside the token; the first line's
        # leading whitespace is outside it and stays reindentable
        freeze(frozen, node.start_point[0] + 1, node.end_point[0])


def freeze_reference_body(node: Node, closer: str, frozen: list[bool]) -> None:
    """A ref block's body is opaque text, like a note."""
    end_row = child_row(node, closer)
    if end_row is not None:
        freeze(frozen, node.start_point[0] + 1, end_row - 1)
