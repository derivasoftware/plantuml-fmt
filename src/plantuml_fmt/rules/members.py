"""A member re-emits as its visibility and modifiers, then its attribute or
method rebuilt; ``member_style`` chooses whether a method keeps its written
direction (preserve, the default) or is moved to canonical or C++."""

from tree_sitter import Node

from plantuml_fmt.rules.attributes import rewrite_attribute
from plantuml_fmt.rules.methods import rewrite_method
from plantuml_fmt.rules.reading import single_line, text

MEMBER_STYLES = ("preserve", "canonical", "cpp")


def rewrite_member(
    src: bytes, node: Node, member_style: str = "preserve"
) -> bytes | None:
    if not single_line(node):
        return None
    visibility: bytes | None = None
    modifiers: list[bytes] = []
    body: bytes | None = None
    for child in node.children:
        kind = child.type
        if kind == "visibility":
            visibility = text(src, child)
        elif kind == "modifier":
            modifiers.append(text(src, child))
        elif kind == "attribute":
            body = rewrite_attribute(src, child)
        elif kind == "method":
            body = rewrite_method(src, child, member_style)
    if body is None:
        return None
    head = [p for p in ([visibility] if visibility else []) + modifiers if p]
    return b" ".join([*head, body]) if head else body
