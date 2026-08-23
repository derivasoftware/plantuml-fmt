"""v1 intra-line style rules: canonical spacing rebuilt from the CST.

Each rewriter re-emits a single-line statement from its node's children
with canonical whitespace between them — the tokens themselves are never
altered, so every rewrite is a whitespace-only change by construction. A
rewriter returns None whenever the line contains anything it cannot
faithfully rebuild (opaque payloads, multi-line spans); the caller then
leaves the line's own spacing untouched.
"""

from tree_sitter import Node


def _text(src: bytes, node: Node) -> bytes:
    return src[node.start_byte:node.end_byte]


def _single_line(node: Node) -> bool:
    end_row = node.end_point[0]
    if node.end_point[1] == 0:
        end_row -= 1
    return node.start_point[0] == end_row


def rewrite_relation(src: bytes, node: Node) -> bytes | None:
    if not _single_line(node):
        return None
    parts: list[bytes] = []
    label: bytes | None = None
    for child in node.children:
        kind = child.type
        if kind == "\n":
            continue
        if kind == "label":
            label = _text(src, child).strip()
        elif kind == ":":
            continue
        elif kind == "role" and parts:
            # roles are adjacent to their cardinality ("owner"/items) —
            # a space would change what re-parses
            parts[-1] += _text(src, child).strip()
        else:
            parts.append(_text(src, child).strip())
    line = b" ".join(p for p in parts if p)
    if label is not None:
        line += b" : " + label
    return line


def rewrite_member(src: bytes, node: Node) -> bytes | None:
    if not _single_line(node):
        return None
    visibility: bytes | None = None
    modifiers: list[bytes] = []
    body: bytes | None = None
    for child in node.children:
        kind = child.type
        if kind == "visibility":
            visibility = _text(src, child)
        elif kind == "modifier":
            modifiers.append(_text(src, child))
        elif kind == "attribute":
            body = _rewrite_attribute(src, child)
        elif kind == "method":
            body = _rewrite_method(src, child)
    if body is None:
        return None
    head = [p for p in ([visibility] if visibility else []) + modifiers if p]
    return b" ".join([*head, body]) if head else body


def _rewrite_attribute(src: bytes, node: Node) -> bytes | None:
    if node.child_by_field_name("text") is not None:
        return None  # free-text member: opaque payload, keep verbatim
    name = node.child_by_field_name("name")
    type_ = node.child_by_field_name("type")
    if name is None:
        return None
    line = _text(src, name)
    if type_ is not None:
        line += b" : " + _text(src, type_).strip()
    return line


def _rewrite_method(src: bytes, node: Node) -> bytes | None:
    name = node.child_by_field_name("name")
    if name is None:
        return None
    params = node.child_by_field_name("parameters")
    rendered = b""
    if params is not None:
        pieces = [
            _text(src, p).strip()
            for p in params.children
            if p.type == "parameter"
        ]
        rendered = b", ".join(pieces)
    line = _text(src, name) + b"(" + rendered + b")"
    type_ = node.child_by_field_name("type")
    if type_ is not None:
        line += b" : " + _text(src, type_).strip()
    return line
