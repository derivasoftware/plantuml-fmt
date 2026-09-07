"""Whitespace-canonicalizing PlantUML formatter (v2).

Three layers of canon, all whitespace-only so the formatter stays
lossless by construction and idempotent (the opt-in member_style is the
one sanctioned exception, REQ-00003-5 / REQ-00012-1 — see rules.py):

- indentation: two spaces per enclosing block or sequence frame;
- intra-line: relations and members rebuilt from the CST with single
  spaces (immediate-adjacency tokens, like cardinality roles, stay
  glued);
- blank lines (v2): runs collapse to one, and blanks touching a block
  or frame edge disappear.

Opaque content — note bodies, raw-block bodies, block-comment
continuation lines — is preserved byte-identical (frozen rows).
"""

from tree_sitter import Node

from plantuml_fmt.rules import (
    MEMBER_STYLES,
    get_parser,
    rewrite_member,
    rewrite_relation,
)

INDENT = b"  "

# Braced blocks whose inner lines gain one indentation level.
_BLOCKS = {
    "entity_body",
    "package_block",
    "namespace_block",
    "together_block",
    "partition_block",
}

# Keyword-closed blocks (grammar 0.10): the direct child that closes
# the block and the clause children whose head line stays at block
# depth, like a frame's else. `repeat` appears twice in a repeat_block
# (opener and `repeat while` closer): the last one is the closer.
_KEYWORD_BLOCKS = {
    "frame_block": ("end", ("else_clause",)),
    "if_block": ("endif", ("elseif_clause", "else_clause")),
    "while_block": ("endwhile", ()),
    "repeat_block": ("repeat", ()),
    "switch_block": ("endswitch", ("case_clause",)),
    "fork_block": ("end", ("fork_again",)),
    "split_block": ("end", ("split_again",)),
    "box_block": ("end box", ()),
    "reference": ("end ref", ()),
}


def _freeze(frozen: list[bool], first_row: int, last_row: int) -> None:
    for row in range(max(first_row, 0), min(last_row + 1, len(frozen))):
        frozen[row] = True


def _child_row(node: Node, child_type: str) -> int | None:
    """Row of the last child of the given type, or None."""
    row = None
    for child in node.children:
        if child.type == child_type:
            row = child.start_point[0]
    return row


def _indent_block(node: Node, depth: list[int]) -> None:
    # the closing-brace row keeps the parent depth; blocks that consume
    # a trailing newline end on the NEXT row, so anchor on the '}' child
    brace_row = _child_row(node, "}")
    if brace_row is None:
        brace_row = node.end_point[0]
    for row in range(node.start_point[0] + 1, brace_row):
        depth[row] += 1


def _indent_frame(
    node: Node, depth: list[int], closer: str, clauses: tuple[str, ...]
) -> None:
    # bodies gain a level; clause heads and the closer stay at block depth
    end_row = _child_row(node, closer)
    if end_row is None:
        end_row = node.end_point[0]
    for row in range(node.start_point[0] + 1, end_row):
        depth[row] += 1
    for child in node.children:
        if child.type in clauses:
            depth[child.start_point[0]] -= 1


def _mark_block_edges(node: Node, openers: set[int], closers: set[int]) -> None:
    openers.add(node.start_point[0])
    brace_row = _child_row(node, "}")
    if brace_row is not None:
        closers.add(brace_row)


def _mark_frame_edges(
    node: Node,
    openers: set[int],
    closers: set[int],
    closer: str,
    clauses: tuple[str, ...],
) -> None:
    openers.add(node.start_point[0])
    end_row = _child_row(node, closer)
    if end_row is not None:
        closers.add(end_row)
    for child in node.children:
        if child.type in clauses:
            openers.add(child.start_point[0])
            closers.add(child.start_point[0])


def _collect(
    node: Node,
    depth: list[int],
    frozen: list[bool],
    rewrites: dict[int, Node],
    openers: set[int],
    closers: set[int],
) -> None:
    kind = node.type
    if kind in _BLOCKS:
        _indent_block(node, depth)
        _mark_block_edges(node, openers, closers)
    elif kind in _KEYWORD_BLOCKS:
        closer, clauses = _KEYWORD_BLOCKS[kind]
        _indent_frame(node, depth, closer, clauses)
        _mark_frame_edges(node, openers, closers, closer, clauses)
        if kind == "reference":
            # the block body is opaque text, like a note
            end_row = _child_row(node, closer)
            if end_row is not None:
                _freeze(frozen, node.start_point[0] + 1, end_row - 1)
    elif kind in ("relation", "member"):
        rewrites[node.start_point[0]] = node
    elif kind == "note_statement":
        end_row = _child_row(node, "end note")
        if end_row is not None:
            _freeze(frozen, node.start_point[0] + 1, end_row - 1)
    elif kind == "raw_block":
        tail_row = _child_row(node, "raw_line")
        if tail_row is not None:
            _freeze(frozen, node.start_point[0] + 1, tail_row - 1)
    elif kind == "block_comment":
        # continuation lines live inside the token; the first line's
        # leading whitespace is outside it and stays reindentable
        _freeze(frozen, node.start_point[0] + 1, node.end_point[0])
    for child in node.children:
        _collect(child, depth, frozen, rewrites, openers, closers)


def _rewrite(node: Node, src: bytes, member_style: str) -> bytes | None:
    if node.type == "relation":
        return rewrite_relation(src, node)
    return rewrite_member(src, node, member_style)


def _is_soft_blank(lines: list[bytes], frozen: list[bool], row: int) -> bool:
    return not lines[row].strip() and not frozen[row]


def _neighbor(row: int, step: int, lines: list[bytes], frozen: list[bool]) -> int:
    """Nearest non-blank row in the given direction, skipping soft blanks."""
    row += step
    while 0 <= row < len(lines) and _is_soft_blank(lines, frozen, row):
        row += step
    return row


def _keep_blank(
    row: int,
    lines: list[bytes],
    frozen: list[bool],
    openers: set[int],
    closers: set[int],
) -> bool:
    """v2 blank-line policy: a run of blank lines collapses to one, and
    blanks touching a block or frame edge disappear entirely. Frozen
    rows (opaque bodies) never reach this decision."""
    prev = _neighbor(row, -1, lines, frozen)
    nxt = _neighbor(row, 1, lines, frozen)
    if prev >= 0 and prev in openers:
        return False
    if nxt < len(lines) and nxt in closers:
        return False
    # collapse: only the first blank of a run survives
    return not (row > 0 and _is_soft_blank(lines, frozen, row - 1))


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
    _collect(tree.root_node, depth, frozen, rewrites, openers, closers)

    out = []
    for row, line in enumerate(lines):
        if frozen[row]:
            out.append(line)
            continue
        stripped = line.lstrip(b" \t")
        if not stripped:
            if _keep_blank(row, lines, frozen, openers, closers):
                out.append(b"")
            continue
        node = rewrites.get(row)
        if node is not None:
            rebuilt = _rewrite(node, src, member_style)
            if rebuilt is not None:
                stripped = rebuilt
        out.append(INDENT * depth[row] + stripped)
    return b"\n".join(out)


def format_text(src: str, member_style: str = "preserve") -> str:
    return format_bytes(src.encode(), member_style).decode()
