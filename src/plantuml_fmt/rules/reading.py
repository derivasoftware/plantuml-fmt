"""Reading the tree: one grammar instance for every document the formatter
reads, and a node read back out of its source — its bytes, and whether it
fits on one line (a rewrite rebuilds single-line statements only)."""

import tree_sitter_plantuml
from tree_sitter import Language, Node, Parser

_parser: Parser | None = None


def get_parser() -> Parser:
    global _parser
    if _parser is None:
        _parser = Parser(Language(tree_sitter_plantuml.language()))
    return _parser


def text(src: bytes, node: Node) -> bytes:
    return src[node.start_byte : node.end_byte]


def single_line(node: Node) -> bool:
    end_row = node.end_point[0]
    if node.end_point[1] == 0:
        end_row -= 1
    return node.start_point[0] == end_row
