"""Relations re-emit with single spaces between their tokens and the label
after a canonical colon; a role stays glued to its cardinality."""

from tree_sitter import Node

from plantuml_fmt.rules.reading import single_line, text


def rewrite_relation(src: bytes, node: Node) -> bytes | None:
    if not single_line(node):
        return None
    parts: list[bytes] = []
    label: bytes | None = None
    for child in node.children:
        kind = child.type
        if kind == "\n":
            continue
        if kind == "label":
            label = text(src, child).strip()
        elif kind == ":":
            continue
        elif kind == "role" and parts:
            # roles are adjacent to their cardinality ("owner"/items) —
            # a space would change what re-parses
            parts[-1] += text(src, child).strip()
        else:
            parts.append(text(src, child).strip())
    line = b" ".join(p for p in parts if p)
    if label is not None:
        line += b" : " + label
    return line
