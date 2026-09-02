"""Opt-in member direction conversion (REQ-00012-1): --member-style
moves a method's type across the name with every other field intact —
and only when the converted line re-parses to the identical signature.
Attributes, prose members and unconvertible signatures keep their
written form; the default remains preserve (REQ-00011-1)."""

from plantuml_fmt.formatter import format_text


def _member(line: str, style: str) -> str:
    src = f"@startuml\nclass C {{\n  {line}\n}}\n@enduml\n"
    out = format_text(src, member_style=style)
    assert format_text(out, member_style=style) == out, "idempotency"
    return out.splitlines()[2].strip()


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


def test_attributes_are_never_converted():
    line = "+ m_cb : std::function<void(int)>"
    assert _member(line, "cpp") == line
    assert _member(line, "canonical") == line


def test_prose_members_pass_through():
    line = "+ Callable Protocol described in words"
    assert _member(line, "canonical") == line
    assert _member(line, "cpp") == line


def test_degenerate_dual_type_is_not_converted():
    line = "+ void f() : int"
    assert _member(line, "canonical") == line
    assert _member(line, "cpp") == line


def test_default_stays_preserve():
    src = "@startuml\nclass C {\n  + void start()\n}\n@enduml\n"
    assert format_text(src) == src
