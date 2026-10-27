"""Opt-in member direction conversion (REQ-00012-1): --member-style
moves a method's type across the name with every other field intact —
and only when the converted line re-parses to the identical signature.
Attributes, prose members and unconvertible signatures keep their
written form; the default remains preserve (REQ-00011-1).

The tests drive the conversion itself (rules.direction) over a parsed
method signature: a refused conversion leaves the signature in its written
direction, re-emitted as the method rewrite would."""

from plantuml_fmt.rules.direction import convert
from tests.integration._grammar import parse
from plantuml_fmt.rules.signature import emit_method, method_signature


def _convert(line: str, style: str) -> str:
    src = f"@startuml\nclass C {{\n  {line}\n}}\n@enduml\n".encode()
    stack = [parse(src).root_node]
    while stack:
        node = stack.pop()
        if node.type == "method":
            sig = method_signature(src, node)
            out = convert(sig, style) or emit_method(sig)
            line_start = src.rfind(b"\n", 0, node.start_byte) + 1
            head = b" ".join(src[line_start : node.start_byte].split())
            return ((head + b" ") if head else b"").decode() + out.decode()
        stack.extend(node.children)
    raise AssertionError(f"no method in {line!r}")


def _member(line: str, style: str) -> str:
    out = _convert(line, style)
    assert _convert(out, style) == out, "idempotency"
    return out


def test_canonical_moves_plain_type_right():
    assert _member("+ void start()", "canonical") == "+ start() : void"


def test_canonical_moves_cpp_type_right():
    assert (
        _member("+ std::vector<T> collect<T, U>(U source)", "canonical")
        == "+ collect<T, U>(U source) : std::vector<T>"
    )


def test_canonical_keeps_suffix_before_the_colon():
    assert _member("+ int f() const", "canonical") == "+ f() const : int"


def test_cpp_moves_plain_type_left():
    assert _member("+ start() : void", "cpp") == "+ void start()"


def test_cpp_moves_qualified_type_left():
    assert _member("+ get_name(): std::string", "cpp") == "+ std::string get_name()"


def test_cpp_refuses_a_type_that_cannot_stand_left():
    # a bracketed Python type does not re-parse left of the name; the
    # guard fails and the member keeps its written direction.
    line = "+ names() : Sequence[str]"
    assert _member(line, "cpp") == line


def test_cpp_refuses_operator_names():
    # `bool operator==(…)` does not re-parse as the same method (the
    # plain-type scanner excludes operator); stays canonical.
    line = "+ operator==(other : T) : bool"
    assert _member(line, "cpp") == line


def test_untyped_method_is_stable_in_both_styles():
    assert _member("+ run()", "canonical") == "+ run()"
    assert _member("+ run()", "cpp") == "+ run()"


def test_degenerate_dual_type_is_not_converted():
    line = "+ void f() : int"
    assert _member(line, "canonical") == line
    assert _member(line, "cpp") == line
