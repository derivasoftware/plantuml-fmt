# Requirements & status

One row per requirement with its state across the V: named by the design,
traced to code, verified, and the real result of its tests (junit
evidence from `test-results/`, produced by `scripts/gen_evidence.py`). The header KPIs aggregate the table.

<!-- folio: status --junit test-results/junit.xml --coverage_ut test-results/coverage-ut.xml --coverage_st test-results/coverage-st.xml -->
**KPIs** (10 requirements): 100% verified · 100% tests passing · 95% UT coverage · 65% ST coverage

| Requirement | Status | Design | Code | VER | Tests |
| --- | --- | --- | --- | --- | --- |
| REQ-00001-1 — The formatter shall indent statements two spaces per enclosing block | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00002-1 — The formatter shall reach a fixed point in a single pass | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00003-4 — The formatter shall change only whitespace, blank lines included | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00004-1 — The formatter shall preserve opaque content byte-identically | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00005-1 — The command-line interface shall report offending files in check mode and rewrite them in write mode | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00006-1 — The repository shall expose the formatter as a pre-commit hook | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00007-2 — The formatter shall normalize relation spacing to single spaces preserving token adjacency | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00008-1 — The formatter shall normalize member spacing and parameter separators | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00009-1 — The formatter shall indent sequence frame bodies | APPROVED | ✓ | ? | ✓ | ✓ pass |
| REQ-00010-1 — The formatter shall collapse blank-line runs and strip blanks at block edges | APPROVED | ✓ | ? | ✓ | ✓ pass |
<!-- /folio -->

The why behind each requirement lives in [rationale.md](rationale.md).
