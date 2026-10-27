"""Parse a snippet and find the first node of a kind."""

from tests.integration._grammar import parse


def parse_first(src: bytes, kind: str):
    stack = [parse(src).root_node]
    while stack:
        node = stack.pop(0)
        if node.type == kind:
            return node
        stack.extend(node.children)
    raise AssertionError(kind)


def all_of(src: bytes, kind: str):
    out, stack = [], [parse(src).root_node]
    while stack:
        node = stack.pop(0)
        if node.type == kind:
            out.append(node)
        stack.extend(node.children)
    return out
