"""Find the first node of a kind in a parsed diagram."""

from plantuml_fmt.rules import get_parser


def first(src: bytes, kind: str):
    stack = [get_parser().parse(src).root_node]
    while stack:
        node = stack.pop(0)
        if node.type == kind:
            return node
        stack.extend(node.children)
    raise AssertionError(kind)
