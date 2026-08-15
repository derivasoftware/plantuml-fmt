# plantuml-fmt

Canonical formatter for [PlantUML](https://plantuml.com/), built on
[tree-sitter-plantuml](https://gitlab.semantiqa.dev/deriva/plantuml/tree-sitter-plantuml).

Part of the `deriva/plantuml` toolchain family: grammar → formatter → LSP.
Each tool consumes the previous one as a versioned package.

## Guarantees

- **Lossless**: only leading horizontal whitespace of statement lines
  changes. Opaque content — note bodies, legend/header/footer and
  `skinparam` block bodies, block-comment continuations, raw frontier
  lines — is preserved byte-identical.
- **Idempotent**: `fmt(fmt(x)) == fmt(x)`, verified by tests.

## Canonical style (v1)

1. Two-space indentation per enclosing block (`{ }` bodies) **and per
   sequence frame** (`alt`/`loop`/… bodies; `else`/`end` at frame depth).
2. Statements outside blocks sit at column 0.
3. Relations: single spaces between endpoints, cardinalities and the
   operator; labels emitted as ` : label`.
4. Members: `visibility {modifiers} name : type`, methods
   `name(p1, p2) : type` with `, `-joined parameters.
5. Anything a rule cannot faithfully rebuild — free-text members, opaque
   bodies, multi-line spans — keeps its own spacing verbatim.

Every rule is a versioned REQ; only whitespace ever changes
(v0 touched leading whitespace only; v1 widened to whole-line).

## Usage

```bash
plantuml-fmt design/            # format in place
plantuml-fmt --check design/    # CI gate: exit 1 if anything would change
```

As a [pre-commit](https://pre-commit.com/) hook:

```yaml
- repo: https://gitlab.semantiqa.dev/deriva/plantuml/plantuml-fmt
  rev: main
  hooks:
    - id: plantuml-fmt
```

## Development

```bash
python3 -m venv .venv && ./.venv/bin/pip install -e ".[dev]"
./.venv/bin/pytest
```

## Governance

An [argos](https://gitlab.semantiqa.dev/deriva/argos/argos) NA project:
input requirements in `input/`, requirements and verifications in
`requirements/` and `verifications/`. See `CLAUDE.md`.
