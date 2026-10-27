"""Intra-line style rules: canonical spacing rebuilt from the CST.

Each rewriter re-emits a single-line statement from its node's children
with canonical whitespace between them — the tokens themselves are never
altered, so every rewrite is a whitespace-only change by construction. A
rewriter returns None whenever the line contains anything it cannot
faithfully rebuild (opaque payloads, multi-line spans); the caller then
leaves the line's own spacing untouched. One file per use case; the
public surface is re-exported here so no importer changes."""

from plantuml_fmt.rules.members import MEMBER_STYLES, rewrite_member
from plantuml_fmt.rules.reading import get_parser
from plantuml_fmt.rules.relations import rewrite_relation

__all__ = ["MEMBER_STYLES", "get_parser", "rewrite_member", "rewrite_relation"]
