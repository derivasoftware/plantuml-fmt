"""Attributes re-emit as name : type; a free-text member stays as written."""

from plantuml_fmt.rules.attributes import rewrite_attribute
from tests.integration.rules._tree import parse_first


def _attr(line: str):
    src = f"@startuml\nclass C {{\n  {line}\n}}\n@enduml\n".encode()
    out = rewrite_attribute(src, parse_first(src, "attribute"))
    return out.decode() if out is not None else None


def test_name_and_type_get_a_canonical_colon():
    assert _attr("-balance:int") == "balance : int"


def test_an_untyped_attribute_is_its_name():
    assert _attr("+ count") == "count"


def test_a_free_text_member_is_not_rebuilt():
    assert _attr("+ Callable Protocol described in words") is None
