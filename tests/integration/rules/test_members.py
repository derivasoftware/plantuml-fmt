"""A member re-emits as visibility and modifiers, then its attribute or
method rebuilt; attributes and prose never reach the direction conversion,
and without a requested style a method keeps its written direction."""

from plantuml_fmt.rules.members import MEMBER_STYLES, rewrite_member
from tests.integration.rules._tree import parse_first


def _member(line: str, style: str = "preserve"):
    src = f"@startuml\nclass C {{\n  {line}\n}}\n@enduml\n".encode()
    out = rewrite_member(src, parse_first(src, "member"), style)
    return out.decode() if out is not None else None


def test_visibility_and_modifiers_lead_with_single_spaces():
    assert (
        _member("+   {static}   deposit( amount:int ,ledger ):void")
        == "+ {static} deposit(amount:int, ledger) : void"
    )


def test_attributes_are_never_converted():
    line = "+ m_cb : std::function<void(int)>"
    for style in MEMBER_STYLES:
        assert _member(line, style) == line


def test_prose_members_pass_through():
    for style in MEMBER_STYLES:
        assert _member("+ Callable Protocol described in words", style) is None


def test_the_default_style_keeps_the_written_direction():
    assert _member("+ void start()") == "+ void start()"
