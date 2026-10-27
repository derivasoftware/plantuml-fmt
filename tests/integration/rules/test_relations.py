"""Relations re-emit with single spaces and a canonical label colon; a role
stays glued to its cardinality, activation shorthand and boundary arrows
keep their tokens."""

from plantuml_fmt.rules.relations import rewrite_relation
from tests.integration.rules._tree import all_of


def _relations(body: str) -> list[str]:
    src = f"@startuml\n{body}\n@enduml\n".encode()
    return [rewrite_relation(src, n).decode() for n in all_of(src, "relation")]


def test_spacing_collapses_and_the_label_gets_its_colon():
    assert _relations("Dog   --|>   Animal:barks\nA -->B") == [
        "Dog --|> Animal : barks",
        "A --> B",
    ]


def test_a_role_stays_glued_to_its_cardinality():
    assert _relations('User   "owner"/1   --   "0..n"/items   Item') == [
        'User "owner"/1 -- "0..n"/items Item'
    ]


def test_activation_shorthand_keeps_its_tokens():
    assert _relations("Alice   ->   Bob   ++   #gold   :   go") == [
        "Alice -> Bob ++ #gold : go"
    ]


def test_boundary_messages_normalize():
    assert _relations("[->   Bob   :   hello\nBob   ->]   :   bye") == [
        "[-> Bob : hello",
        "Bob ->] : bye",
    ]
