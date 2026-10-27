"""A grammar instance of the tests' own, so building a fixture tree never
runs the formatter's shared reader (rules.reading) under another
requirement's tests."""

import tree_sitter_plantuml
from tree_sitter import Language, Parser

_parser = Parser(Language(tree_sitter_plantuml.language()))


def parse(src: bytes):
    return _parser.parse(src)
