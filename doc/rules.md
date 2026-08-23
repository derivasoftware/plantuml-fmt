# Canonical style — the versioned rulebook

Every rule is a versioned REQ in this repo's GDD; the style only ever
changes by revising those artefacts. Two invariants bound every rule,
present and future:

- **Lossless**: only whitespace of statement lines changes; every
  non-whitespace byte is preserved in order.
- **Idempotent**: `fmt(fmt(x)) == fmt(x)` (tested).

## v1 rules

**R1 — indentation.** Two spaces per enclosing `{ }` body and per
sequence frame; `else`/`end` sit at frame depth; statements outside
blocks at column 0.

```
@startuml                        @startuml
  class A {                      class A {
        +run():int                 +run() : int
  }                              }
@enduml                          @enduml
```

**R2 — relations.** Single spaces between endpoints, cardinalities and
operator; labels as ` : label`.

```
A"1"*--"many"B:owns       →     A "1" *-- "many" B : owns
```

**R3 — members.** `visibility {modifiers} name : type`; methods
`name(p1, p2) : type` with `, `-joined parameters.

```
+  run( a:int ,b:str ):int  →   + run(a:int, b:str) : int
```

**R4 — opacity.** Anything a rule cannot faithfully rebuild keeps its
spacing verbatim: free-text members, note bodies, `legend`/`header`/
`footer` and braced `skinparam` bodies, block-comment continuations,
raw frontier lines.

## Adding a rule

1. Corpus case first (before/after) — RED.
2. Rule implementation over the CST (never regex over text).
3. Idempotence + losslessness suites green.
4. New REQ (or revision) + VER; note the style version bump in the
   README (v0 touched leading whitespace only; v1 widened to
   whole-line).

## Boundary with the LSP

`plantuml-lsp` delegates `textDocument/formatting` here — one
implementation of the style, however it is invoked (CLI, pre-commit,
editor).
