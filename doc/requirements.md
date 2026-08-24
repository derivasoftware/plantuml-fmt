# Requirements & status

One row per requirement with its state across the V: named by the design,
traced to code, verified, and the real result of its tests (junit evidence
from the last CI run; the wiring is in progress, so results read unknown
for now). The header KPIs aggregate the table.

<!-- folio: status -->
**KPIs** (10 requirements): 100% verified

| Requirement | Status | Design | Code | VER | Tests |
| --- | --- | --- | --- | --- | --- |
| REQ-00001-1 — The formatter shall indent statements two spaces per enclosing block | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00002-1 — The formatter shall reach a fixed point in a single pass | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00003-3 — The formatter shall change only whitespace, blank lines included | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00004-1 — The formatter shall preserve opaque content byte-identically | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00005-1 — The command-line interface shall report offending files in check mode and rewrite them in write mode | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00006-1 — The repository shall expose the formatter as a pre-commit hook | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00007-2 — The formatter shall normalize relation spacing to single spaces preserving token adjacency | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00008-1 — The formatter shall normalize member spacing and parameter separators | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00009-1 — The formatter shall indent sequence frame bodies | APPROVED | ✓ | ? | ✓ | ? |
| REQ-00010-1 — The formatter shall collapse blank-line runs and strip blanks at block edges | APPROVED | ✓ | ? | ✓ | ? |
<!-- /folio -->

The why behind each requirement lives in [rationale.md](rationale.md).
