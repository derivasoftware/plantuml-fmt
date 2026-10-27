"""Whitespace-canonicalizing PlantUML formatter (v2): one pass over the
syntax tree, then one rewrite per line.

Three layers of canon, all whitespace-only so the formatter stays
lossless by construction and idempotent (the opt-in member_style is the
one sanctioned exception, CST-00001-1 / REQ-00012-1 — see rules):

- indentation: two spaces per enclosing block (blocks) or sequence frame
  (frames);
- intra-line: relations and members rebuilt from the CST with single
  spaces (immediate-adjacency tokens, like cardinality roles, stay
  glued); a line the rewrite does not cover keeps its bytes;
- blank lines (blanks): runs collapse to one, and blanks touching a block
  or frame edge disappear.

Opaque content — note bodies, raw-block bodies, block-comment
continuation lines — is preserved byte-identical (opaque).
"""

from tree_sitter import Node

from plantuml_fmt.formatter.blanks import keep_blank
from plantuml_fmt.formatter.blocks import BLOCKS, indent_block, mark_block_edges
from plantuml_fmt.formatter.frames import KEYWORD_BLOCKS, indent_frame, mark_frame_edges
from plantuml_fmt.formatter.opaque import freeze_opaque, freeze_reference_body
from plantuml_fmt.rules import (
    MEMBER_STYLES,
    get_parser,
    rewrite_member,
    rewrite_relation,
)

INDENT = b"  "


def collect(
    node: Node,
    depth: list[int],
    frozen: list[bool],
    rewrites: dict[int, Node],
    openers: set[int],
    closers: set[int],
) -> None:
    kind = node.type
    if kind in BLOCKS:
        indent_block(node, depth)
        mark_block_edges(node, openers, closers)
    elif kind in KEYWORD_BLOCKS:
        closer, clauses = KEYWORD_BLOCKS[kind]
        indent_frame(node, depth, closer, clauses)
        mark_frame_edges(node, openers, closers, closer, clauses)
        if kind == "reference":
            freeze_reference_body(node, closer, frozen)
    elif kind in ("relation", "member"):
        rewrites[node.start_point[0]] = node
    else:
        freeze_opaque(node, kind, frozen)
    for child in node.children:
        collect(child, depth, frozen, rewrites, openers, closers)


def rewrite(node: Node, src: bytes, member_style: str) -> bytes | None:
    if node.type == "relation":
        return rewrite_relation(src, node)
    return rewrite_member(src, node, member_style)


def spans_line(node: Node, row: int, line: bytes) -> bool:
    """Whether the node holds every non-whitespace byte of its line: a rewrite
    re-emits the node alone, so a line it does not cover keeps its bytes."""
    if node.start_point[1] != len(line) - len(line.lstrip(b" \t")):
        return False
    if node.end_point[0] != row:
        return True
    return not line[node.end_point[1] :].strip()


def format_bytes(src: bytes, member_style: str = "preserve") -> bytes:
    if member_style not in MEMBER_STYLES:
        raise ValueError(f"unknown member_style: {member_style!r}")
    tree = get_parser().parse(src)
    lines = src.split(b"\n")
    depth = [0] * len(lines)
    frozen = [False] * len(lines)
    rewrites: dict[int, Node] = {}
    openers: set[int] = set()
    closers: set[int] = set()
    collect(tree.root_node, depth, frozen, rewrites, openers, closers)

    out = []
    for row, line in enumerate(lines):
        if frozen[row]:
            out.append(line)
            continue
        stripped = line.lstrip(b" \t")
        if not stripped:
            if keep_blank(row, lines, frozen, openers, closers):
                out.append(b"")
            continue
        node = rewrites.get(row)
        if node is not None and spans_line(node, row, line):
            rebuilt = rewrite(node, src, member_style)
            if rebuilt is not None:
                stripped = rebuilt
        out.append(INDENT * depth[row] + stripped)
    return b"\n".join(out)


def format_text(src: str, member_style: str = "preserve") -> str:
    return format_bytes(src.encode(), member_style).decode()
