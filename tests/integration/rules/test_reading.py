"""One grammar instance reads every document, and a node reads back its
bytes and whether it fits on one line."""

from plantuml_fmt.rules.reading import get_parser, single_line, text
from tests.integration.rules._tree import parse_first


def test_every_caller_shares_one_grammar_instance():
    assert get_parser() is get_parser()


def test_the_grammar_reads_a_diagram_without_error():
    tree = get_parser().parse(
        b"@startuml\nclass A {\n+x : int\n}\nA --> B : uses\n@enduml\n"
    )
    assert not tree.root_node.has_error


def test_a_node_reads_back_its_own_bytes():
    src = b"@startuml\nDog --|> Animal : barks\n@enduml\n"
    assert text(src, parse_first(src, "label")) == b"barks"


def test_a_statement_with_its_newline_still_fits_one_line():
    src = b"@startuml\nA --> B\n@enduml\n"
    assert single_line(parse_first(src, "relation"))


def test_a_block_spanning_rows_does_not():
    src = b"@startuml\nclass A {\n+x : int\n}\n@enduml\n"
    assert not single_line(parse_first(src, "entity_body"))
