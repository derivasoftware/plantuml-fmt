"""Per-statement rules: relations and members rebuilt with canonical spacing."""

from plantuml_fmt.rules import get_parser, rewrite_member, rewrite_relation

__covers__ = (get_parser, rewrite_relation, rewrite_member)


def _first(src: bytes, kind: str):
    stack = [get_parser().parse(src).root_node]
    while stack:
        node = stack.pop(0)
        if node.type == kind:
            return node
        stack.extend(node.children)
    raise AssertionError(f"no {kind}")


class TestGetParser:
    def test_is_built_once(self) -> None:
        assert get_parser() is get_parser()


class TestRewriteRelation:
    def test_single_spaces_around_the_arrow_and_the_label(self) -> None:
        src = b"@startuml\nA   -->    B :   uses\n@enduml\n"
        assert rewrite_relation(src, _first(src, "relation")) == b"A --> B : uses"

    def test_a_role_stays_glued_to_its_cardinality(self) -> None:
        src = b'@startuml\nA "1"   --> "*" B\n@enduml\n'
        assert rewrite_relation(src, _first(src, "relation")) == b'A "1" --> "*" B'


class TestRewriteMember:
    def test_spacing_and_parameter_separators(self) -> None:
        src = b"@startuml\nclass A {\n+  go( a ,b )   : int\n}\n@enduml\n"
        assert rewrite_member(src, _first(src, "member")) == b"+ go(a, b) : int"

    def test_a_cpp_signature_keeps_its_direction_by_default(self) -> None:
        src = b"@startuml\nclass A {\n+int go(int a)\n}\n@enduml\n"
        assert b"int go(" in rewrite_member(src, _first(src, "member"))

    def test_the_canonical_style_moves_the_type_after_the_name(self) -> None:
        src = b"@startuml\nclass A {\n+int go(int a)\n}\n@enduml\n"
        out = rewrite_member(src, _first(src, "member"), "canonical")
        assert out.endswith(b": int")
