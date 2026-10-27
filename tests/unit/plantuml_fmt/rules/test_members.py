"""A member rebuilt as its head and its attribute or method."""

from plantuml_fmt.rules.members import rewrite_member
from tests.unit.plantuml_fmt.rules._tree import first

__covers__ = (rewrite_member,)


class TestRewriteMember:
    def test_spacing_and_parameter_separators(self) -> None:
        src = b"@startuml\nclass A {\n+  go( a ,b )   : int\n}\n@enduml\n"
        assert rewrite_member(src, first(src, "member")) == b"+ go(a, b) : int"

    def test_a_cpp_signature_keeps_its_direction_by_default(self) -> None:
        src = b"@startuml\nclass A {\n+int go(int a)\n}\n@enduml\n"
        assert b"int go(" in rewrite_member(src, first(src, "member"))

    def test_the_canonical_style_moves_the_type_after_the_name(self) -> None:
        src = b"@startuml\nclass A {\n+int go(int a)\n}\n@enduml\n"
        out = rewrite_member(src, first(src, "member"), "canonical")
        assert out.endswith(b": int")
