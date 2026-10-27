"""Methods re-emit their signature in its written direction with canonical
spacing, every field kept; a requested member style may move the type
across the name (direction)."""

from tree_sitter import Node

from plantuml_fmt.rules.direction import convert
from plantuml_fmt.rules.signature import emit_method, method_signature


def rewrite_method(
    src: bytes, node: Node, member_style: str = "preserve"
) -> bytes | None:
    sig = method_signature(src, node)
    if sig is None:
        return None
    converted = convert(sig, member_style)
    return converted if converted is not None else emit_method(sig)
