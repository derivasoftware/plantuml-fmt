"""The v2 blank-line policy: a run of blank lines collapses to one, and
blanks touching a block or frame edge disappear entirely."""


def is_soft_blank(lines: list[bytes], frozen: list[bool], row: int) -> bool:
    return not lines[row].strip() and not frozen[row]


def neighbor(row: int, step: int, lines: list[bytes], frozen: list[bool]) -> int:
    """Nearest non-blank row in the given direction, skipping soft blanks."""
    row += step
    while 0 <= row < len(lines) and is_soft_blank(lines, frozen, row):
        row += step
    return row


def keep_blank(
    row: int,
    lines: list[bytes],
    frozen: list[bool],
    openers: set[int],
    closers: set[int],
) -> bool:
    """Whether a blank row survives. Frozen rows (opaque bodies) never reach
    this decision."""
    prev = neighbor(row, -1, lines, frozen)
    nxt = neighbor(row, 1, lines, frozen)
    if prev >= 0 and prev in openers:
        return False
    if nxt < len(lines) and nxt in closers:
        return False
    # collapse: only the first blank of a run survives
    return not (row > 0 and is_soft_blank(lines, frozen, row - 1))
