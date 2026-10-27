"""An attribute rebuilt as name : type."""

from plantuml_fmt.rules.attributes import rewrite_attribute
from tests.unit.plantuml_fmt.rules._tree import first

__covers__ = (rewrite_attribute,)


class TestRewriteAttribute:
    def test_name_colon_type(self) -> None:
        src = b"@startuml\nclass A {\n-x:int\n}\n@enduml\n"
        assert rewrite_attribute(src, first(src, "attribute")) == b"x : int"

    def test_free_text_is_left_to_the_caller(self) -> None:
        src = b"@startuml\nclass A {\n+ free words here\n}\n@enduml\n"
        assert rewrite_attribute(src, first(src, "attribute")) is None
