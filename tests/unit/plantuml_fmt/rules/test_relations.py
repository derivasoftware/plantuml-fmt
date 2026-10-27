"""A relation rebuilt with canonical spacing."""

from plantuml_fmt.rules.relations import rewrite_relation
from tests.unit.plantuml_fmt.rules._tree import first

__covers__ = (rewrite_relation,)


class TestRewriteRelation:
    def test_single_spaces_around_the_arrow_and_the_label(self) -> None:
        src = b"@startuml\nA   -->    B :   uses\n@enduml\n"
        assert rewrite_relation(src, first(src, "relation")) == b"A --> B : uses"

    def test_a_role_stays_glued_to_its_cardinality(self) -> None:
        src = b'@startuml\nA "1"   --> "*" B\n@enduml\n'
        assert rewrite_relation(src, first(src, "relation")) == b'A "1" --> "*" B'
