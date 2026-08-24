# Release report

What the last release delivered, computed from the repository's own
history: artefact changes by type, requirements delivered with their
verification and commit, technical debt introduced or resolved, and the
commit log for the range.

<!-- folio: report --since v0.2.3 --until v0.3.2 -->
# Project report

**4b1b3924 → 51abc629**  ·  6 commits  ·  2026-08-23 → 2026-08-24

## Summary

| Artefact type | added | modified | removed | status |
| --- | --- | --- | --- | --- |
| Requirements | 1 | 2 | 0 | 0 |
| Verifications | 1 | 0 | 0 | 0 |
| Free functions | 5 | 0 | 0 | 0 |
| Test cases | 9 | 0 | 0 | 0 |

## Delivered requirements

| Requirement | Verification | Commit | Author |
| --- | --- | --- | --- |
| REQ-00010-1 | VER-00010-1 | — | — |

## Artefact changes by type

### Requirements
- modified REQ-00003-2 → REQ-00003-3
- modified REQ-00007-1 → REQ-00007-2
- added REQ-00010-1

### Verifications
- added VER-00010-1

### Free functions
- added plantuml_fmt.formatter._is_soft_blank
- added plantuml_fmt.formatter._keep_blank
- added plantuml_fmt.formatter._mark_block_edges
- added plantuml_fmt.formatter._mark_frame_edges
- added plantuml_fmt.formatter._neighbor

### Test cases
- 9 added

## Commit log

- `51abc629` **David Coello** · Merge branch 'chore/grammar-0.8.0' into 'main'
- `05e84798` **dcoello-dev** · Repin tree-sitter-plantuml to v0.8.0 (0.3.2)
- `24f17ed5` **David Coello** · Merge branch 'chore/grammar-0.7.0' into 'main'
- `b6c14ba0` **dcoello-dev** · Repin tree-sitter-plantuml to v0.7.0 (0.3.1)
- `00832fdc` **David Coello** · Merge branch 'feat/fmt-v2' into 'main'
- `1084fb3c` **dcoello-dev** · fmt v2: blank-line policy, adjacency-preserving rebuilds (0.3.0)
<!-- /folio -->
