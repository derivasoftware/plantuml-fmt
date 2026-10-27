"""Attributes re-emit as ``name : type``; a free-text member is an opaque
payload and is kept as written."""

from tree_sitter import Node

from plantuml_fmt.rules.reading import text


def rewrite_attribute(src: bytes, node: Node) -> bytes | None:
    if node.child_by_field_name("text") is not None:
        return None  # free-text member: opaque payload, keep verbatim
    name = node.child_by_field_name("name")
    type_ = node.child_by_field_name("type")
    if name is None:
        return None
    line = text(src, name)
    if type_ is not None:
        line += b" : " + text(src, type_).strip()
    return line
