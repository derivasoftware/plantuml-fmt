"""Keyword-closed blocks — sequence frames and activity control flow: their
bodies gain a level, clause heads and the closer stay at block depth."""

from tree_sitter import Node

from plantuml_fmt.formatter.rows import child_row

# The direct child that closes the block and the clause children whose head
# line stays at block depth, like a frame's else. `repeat` appears twice in a
# repeat_block (opener and `repeat while` closer): the last one is the closer.
KEYWORD_BLOCKS = {
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


def indent_frame(
    node: Node, depth: list[int], closer: str, clauses: tuple[str, ...]
) -> None:
    # bodies gain a level; clause heads and the closer stay at block depth
    end_row = child_row(node, closer)
    if end_row is None:
        end_row = node.end_point[0]
    for row in range(node.start_point[0] + 1, end_row):
        depth[row] += 1
    for child in node.children:
        if child.type in clauses:
            depth[child.start_point[0]] -= 1


def mark_frame_edges(
    node: Node,
    openers: set[int],
    closers: set[int],
    closer: str,
    clauses: tuple[str, ...],
) -> None:
    openers.add(node.start_point[0])
    end_row = child_row(node, closer)
    if end_row is not None:
        closers.add(end_row)
    for child in node.children:
        if child.type in clauses:
            openers.add(child.start_point[0])
            closers.add(child.start_point[0])
