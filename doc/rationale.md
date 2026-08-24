# Rationale

Every requirement's why, written at decision time, in tree order.

<!-- folio: rationale -->
## SREQ-00001-1 — The tool shall format PlantUML sources into a canonical style

Umbrella: a deterministic, versioned canonical style for PlantUML text, built on the tree-sitter-plantuml grammar. The formatter is the second product of the deriva/plantuml toolchain family.

### REQ-00001-1 — The formatter shall indent statements two spaces per enclosing block

The first versioned style rule: two spaces per braced block, statements at column zero outside blocks.

### REQ-00007-2 — The formatter shall normalize relation spacing to single spaces preserving token adjacency

Endpoints, cardinalities, qualifiers, operators, activations and colors separated by single spaces; labels emitted as ' : label'. Tokens the grammar binds by immediate adjacency — role suffixes on cardinalities ("owner"/items) — stay glued: a space there changes what re-parses. Revision 2 extends the v1 rule to the sequence-era relation children (grammar 0.6+) and records the adjacency exception.

### REQ-00008-1 — The formatter shall normalize member spacing and parameter separators

Visibility, modifiers, name, ' : type' and ', '-joined parameters with canonical spacing; free-text members are opaque payloads and stay verbatim.

### REQ-00009-1 — The formatter shall indent sequence frame bodies

Frame bodies gain one level like braced blocks; else and end lines stay at frame depth. Extends the v0 indentation rule to the v0.2.0 grammar's sequence frames.

### REQ-00010-1 — The formatter shall collapse blank-line runs and strip blanks at block edges

A run of consecutive blank lines collapses to one; blank lines directly after a block or frame opener ({, frame head, else) or directly before its closer (}, end, else) disappear. Blank lines inside opaque bodies (notes, raw blocks) are frozen rows and never reach the policy. Single blank lines between statements are kept — the policy removes noise, it never inserts.

### SREQ-00002-1 — The formatter shall preserve every input token byte-identically

Only whitespace may change between input and output; everything after the first non-whitespace byte of a line is untouchable in v0. Losslessness is what makes a formatter safe to run unattended in pre-commit.

#### REQ-00003-3 — The formatter shall change only whitespace, blank lines included

Losslessness by construction: rewriters re-emit the CST tokens with canonical whitespace between them and refuse any line they cannot faithfully rebuild; the blank-line policy only drops or keeps empty lines. Revision 3 widens the charter from statement-line whitespace to inter-line whitespace, which is what the blank-line policy requires. The wild-corpus eval (scripts/eval_wild_corpus.py) asserts both invariants over every diagram it can find.

### SREQ-00003-1 — The formatter shall emit identical output when reformatting its own output

Idempotency: fmt(fmt(x)) == fmt(x) for every input. A non-idempotent formatter oscillates in CI and erodes trust immediately.

#### REQ-00002-1 — The formatter shall reach a fixed point in a single pass

fmt(fmt(x)) == fmt(x); a formatter that oscillates is unusable in pre-commit.

### SREQ-00004-1 — The formatter shall pass opaque content through verbatim

Note bodies, raw-block bodies (legend, header, footer, skinparam), block-comment continuations and raw frontier lines are opaque per the grammar contract (raw nodes) and must survive byte-identical, indentation included — PlantUML renders note text as-is.

#### REQ-00004-1 — The formatter shall preserve opaque content byte-identically

Note bodies, raw-block bodies and block-comment continuations render as-is in PlantUML; even their indentation is content.

### SREQ-00005-1 — The tool shall provide a command-line interface with check and write modes

plantuml-fmt <paths> writes in place; --check writes nothing, lists offending files and exits nonzero, which is the CI/DoD gate form.

#### REQ-00005-1 — The command-line interface shall report offending files in check mode and rewrite them in write mode

--check is the CI gate (exit 1, list files, write nothing); the default mode formats in place.

### SREQ-00006-1 — The tool shall provide a pre-commit hook

A .pre-commit-hooks.yaml at the repo root so consumers pin the repo and get formatting on commit — the primary distribution channel for a formatter.

#### REQ-00006-1 — The repository shall expose the formatter as a pre-commit hook

A .pre-commit-hooks.yaml at the root wired to the console script is the primary distribution channel.

### SREQ-00007-1 — The tool shall version its canonical style rules

Every style rule (indentation width, future intra-line spacing) is an explicit, documented, versioned decision; style changes are breaking for downstream diffs and follow semver.

#### REQ-00001-1 — The formatter shall indent statements two spaces per enclosing block

The first versioned style rule: two spaces per braced block, statements at column zero outside blocks.

#### REQ-00007-2 — The formatter shall normalize relation spacing to single spaces preserving token adjacency

Endpoints, cardinalities, qualifiers, operators, activations and colors separated by single spaces; labels emitted as ' : label'. Tokens the grammar binds by immediate adjacency — role suffixes on cardinalities ("owner"/items) — stay glued: a space there changes what re-parses. Revision 2 extends the v1 rule to the sequence-era relation children (grammar 0.6+) and records the adjacency exception.

#### REQ-00008-1 — The formatter shall normalize member spacing and parameter separators

Visibility, modifiers, name, ' : type' and ', '-joined parameters with canonical spacing; free-text members are opaque payloads and stay verbatim.

#### REQ-00009-1 — The formatter shall indent sequence frame bodies

Frame bodies gain one level like braced blocks; else and end lines stay at frame depth. Extends the v0 indentation rule to the v0.2.0 grammar's sequence frames.
<!-- /folio -->
