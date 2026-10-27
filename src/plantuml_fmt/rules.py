"""v1 intra-line style rules: canonical spacing rebuilt from the CST.

Each rewriter re-emits a single-line statement from its node's children
with canonical whitespace between them — the tokens themselves are never
altered, so every rewrite is a whitespace-only change by construction. A
rewriter returns None whenever the line contains anything it cannot
faithfully rebuild (opaque payloads, multi-line spans); the caller then
leaves the line's own spacing untouched.

The one sanctioned exception to whitespace-only (CST-00001-1) is the
opt-in member style (REQ-00012-1): a method signature may be re-emitted
in a requested direction — canonical ``name(args) : type`` or C++
``type name(args)`` — moving the type across the name with every other
field (template parameters, parameters, trailing qualifiers) intact. A
conversion only stands when the converted line re-parses to the
identical signature; otherwise the member keeps its written direction,
exactly as ``preserve`` does. Attributes and prose members are never
touched: what separates a method from an attribute is the paren pinned
to the name, and the style knob must not blur that frontier.
"""

import tree_sitter_plantuml
from tree_sitter import Language, Node, Parser

MEMBER_STYLES = ("preserve", "canonical", "cpp")

_parser: Parser | None = None


def get_parser() -> Parser:
    global _parser
    if _parser is None:
        _parser = Parser(Language(tree_sitter_plantuml.language()))
    return _parser


def _text(src: bytes, node: Node) -> bytes:
    return src[node.start_byte : node.end_byte]


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


def rewrite_member(
    src: bytes, node: Node, member_style: str = "preserve"
) -> bytes | None:
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
            body = _rewrite_method(src, child, member_style)
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


def _method_signature(src: bytes, node: Node) -> dict | None:
    """Every field of a method, as canonical-whitespace texts.

    The type may sit on either side of the name — a C++ return type or
    plain identifier to the left, the canonical colon type to the right
    — and a degenerate line may carry both; the signature keeps the
    sides apart so nothing is dropped.
    """
    name = node.child_by_field_name("name")
    if name is None:
        return None
    left: bytes | None = None
    right: bytes | None = None
    for type_ in node.children_by_field_name("type"):
        if type_.start_byte < name.start_byte:
            left = _text(src, type_).strip()
        else:
            right = _text(src, type_).strip()
    tparams = node.child_by_field_name("template_parameters")
    params_node = node.child_by_field_name("parameters")
    suffix = node.child_by_field_name("suffix")
    return {
        "left": left,
        "right": right,
        "name": _text(src, name),
        "tparams": _text(src, tparams) if tparams is not None else None,
        "params": tuple(
            _text(src, p).strip()
            for p in (params_node.children if params_node is not None else ())
            if p.type == "parameter"
        ),
        "suffix": (
            b" ".join(_text(src, suffix).split()) if suffix is not None else None
        ),
    }


def _emit_method(sig: dict) -> bytes:
    line = (
        sig["name"] + (sig["tparams"] or b"") + b"(" + b", ".join(sig["params"]) + b")"
    )
    if sig["left"] is not None:
        line = sig["left"] + b" " + line
    if sig["suffix"] is not None:
        line += b" " + sig["suffix"]
    if sig["right"] is not None:
        line += b" : " + sig["right"]
    return line


def _signature_key(sig: dict) -> tuple:
    """Direction-blind identity: the type counts wherever it sits."""
    return (
        sig["left"] if sig["left"] is not None else sig["right"],
        sig["name"],
        sig["tparams"],
        sig["params"],
        sig["suffix"],
    )


def _converts_faithfully(candidate: bytes, want: tuple) -> bool:
    """True iff the candidate re-parses as one method with the wanted
    signature. The grammar is the arbiter: a type the target direction
    cannot express (bracketed forms, prose, operator collisions) fails
    here and the member keeps its written direction."""
    snippet = b"@startuml\nclass _G {\n  " + candidate + b"\n}\n@enduml\n"
    tree = get_parser().parse(snippet)
    if tree.root_node.has_error:
        return False
    methods: list[Node] = []
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        if node.type == "method":
            methods.append(node)
        stack.extend(node.children)
    if len(methods) != 1:
        return False
    got = _method_signature(snippet, methods[0])
    return got is not None and _signature_key(got) == want


def _rewrite_method(
    src: bytes, node: Node, member_style: str = "preserve"
) -> bytes | None:
    sig = _method_signature(src, node)
    if sig is None:
        return None
    if member_style == "canonical" and sig["left"] is not None and sig["right"] is None:
        candidate = _emit_method({**sig, "left": None, "right": sig["left"]})
        if _converts_faithfully(candidate, _signature_key(sig)):
            return candidate
    elif member_style == "cpp" and sig["right"] is not None and sig["left"] is None:
        candidate = _emit_method({**sig, "left": sig["right"], "right": None})
        if _converts_faithfully(candidate, _signature_key(sig)):
            return candidate
    return _emit_method(sig)
