"""The opt-in member style (REQ-00012-1), the one sanctioned exception to
whitespace-only (CST-00001-1): a method signature may be re-emitted in a
requested direction — canonical ``name(args) : type`` or C++
``type name(args)`` — moving the type across the name with every other
field (template parameters, parameters, trailing qualifiers) intact. A
conversion only stands when the converted line re-parses to the identical
signature; otherwise the member keeps its written direction, exactly as
``preserve`` does."""

from tree_sitter import Node

from plantuml_fmt.rules.reading import get_parser
from plantuml_fmt.rules.signature import emit_method, method_signature, signature_key


def converts_faithfully(candidate: bytes, want: tuple) -> bool:
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
    got = method_signature(snippet, methods[0])
    return got is not None and signature_key(got) == want


def convert(sig: dict, member_style: str) -> bytes | None:
    """The signature re-emitted in the requested direction, or None when the
    style asks for no move or the move would not re-parse faithfully."""
    if member_style == "canonical" and sig["left"] is not None and sig["right"] is None:
        candidate = emit_method({**sig, "left": None, "right": sig["left"]})
    elif member_style == "cpp" and sig["right"] is not None and sig["left"] is None:
        candidate = emit_method({**sig, "left": sig["right"], "right": None})
    else:
        return None
    return candidate if converts_faithfully(candidate, signature_key(sig)) else None
