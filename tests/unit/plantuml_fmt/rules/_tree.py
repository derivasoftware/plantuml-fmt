"""Find the first node of a kind in a parsed snippet."""

from plantuml_fmt.rules.reading import get_parser


def first(src: bytes, kind: str):
    stack = [get_parser().parse(src).root_node]
    while stack:
        node = stack.pop(0)
        if node.type == kind:
            return node
        stack.extend(node.children)
    raise AssertionError(f"no {kind}")


def method_in(line: bytes):
    src = b"@startuml\nclass A {\n" + line + b"\n}\n@enduml\n"
    return src, first(src, "method")
