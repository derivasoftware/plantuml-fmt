# Canonical style — the versioned rulebook

Every rule is a versioned REQ in this repo's GDD; the style only ever
changes by revising those artefacts. Two invariants bound every rule,
present and future, as constraints of the rewrite category:

- **Lossless** (CST-00001-1): only whitespace of statement lines changes;
  every non-whitespace byte is preserved in order. A statement a rewrite
  cannot rebuild faithfully, or a line it does not cover whole, keeps its
  bytes (CST-00002-1).
- **Idempotent**: `fmt(fmt(x)) == fmt(x)`.

Both are system needs of the formatter (SREQ-00002-2, SREQ-00003-1),
demonstrated over a real diagram tree by the system pass.

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

## v2 rules

**R5 — blank lines.** A run of consecutive blank lines collapses to
one; blanks directly after a block/frame opener (`{`, frame head,
`else`) or directly before its closer (`}`, `end`, `else`) disappear.
Single blank lines between statements survive — the policy removes
noise, it never inserts. Blank lines inside opaque bodies are untouched.

```
class A {          class A {
                     + x : int
  +x : int         }

}                  class B


class B
```

**R6 — token adjacency.** Single-space normalization never separates
tokens the grammar binds by immediate adjacency: `"owner"/items` role
suffixes stay glued — a space there changes what re-parses.

**R7 — member direction (opt-in).** `--member-style canonical` moves a
method's type after the name (`name(args) : type`), `--member-style cpp`
before it (`type name(args)`), with template parameters, parameters and
trailing qualifiers intact. A conversion stands only when the converted
line re-parses to the identical signature; otherwise the member keeps its
written direction. Attributes and prose members are never converted, and
the default, `preserve`, changes no direction. The one sanctioned
exception to whitespace-only.

```
+ void start()   --member-style canonical →   + start() : void
```

Both invariants are asserted in the wild on demand by the system pass,
over this repository's design tree or any corpus you name:

```bash
PLANTUML_FMT_CORPUS=<root>:<root> .venv/bin/python -m pytest -m system
```
