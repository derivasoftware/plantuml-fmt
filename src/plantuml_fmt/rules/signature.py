"""A method's signature as canonical-whitespace fields, re-emitted in the
direction its fields say, and its direction-blind identity."""

from tree_sitter import Node

from plantuml_fmt.rules.reading import text


def method_signature(src: bytes, node: Node) -> dict | None:
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
            left = text(src, type_).strip()
        else:
            right = text(src, type_).strip()
    tparams = node.child_by_field_name("template_parameters")
    params_node = node.child_by_field_name("parameters")
    suffix = node.child_by_field_name("suffix")
    return {
        "left": left,
        "right": right,
        "name": text(src, name),
        "tparams": text(src, tparams) if tparams is not None else None,
        "params": tuple(
            text(src, p).strip()
            for p in (params_node.children if params_node is not None else ())
            if p.type == "parameter"
        ),
        "suffix": (
            b" ".join(text(src, suffix).split()) if suffix is not None else None
        ),
    }


def emit_method(sig: dict) -> bytes:
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


def signature_key(sig: dict) -> tuple:
    """Direction-blind identity: the type counts wherever it sits."""
    return (
        sig["left"] if sig["left"] is not None else sig["right"],
        sig["name"],
        sig["tparams"],
        sig["params"],
        sig["suffix"],
    )
