#!/usr/bin/env python3
"""Format every .puml under the given roots; assert the two invariants
hold in the wild: losslessness (non-whitespace bytes preserved in
order) and idempotence. Reports how many files would change.

Usage: .venv/bin/python scripts/eval_wild_corpus.py <root> [<root>...]
"""

import pathlib
import sys

from plantuml_fmt.formatter import format_bytes

SKIP_DIRS = {"node_modules", ".venv", ".git", "build"}


def non_ws(data: bytes) -> bytes:
    return b"".join(data.split())


def main(roots: list[str]) -> int:
    total = changed = lossy = unstable = 0
    for root in roots:
        for path in pathlib.Path(root).rglob("*.puml"):
            if SKIP_DIRS & set(path.parts):
                continue
            total += 1
            src = path.read_bytes()
            once = format_bytes(src)
            if non_ws(once) != non_ws(src):
                lossy += 1
                print(f"LOSSY: {path}")
            if format_bytes(once) != once:
                unstable += 1
                print(f"UNSTABLE: {path}")
            if once != src:
                changed += 1
    print(
        f"files: {total}  would-change: {changed}  "
        f"lossy: {lossy}  unstable: {unstable}"
    )
    return 1 if (lossy or unstable) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
