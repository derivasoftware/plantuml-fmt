# plantuml-fmt

Canonical formatter for [PlantUML](https://plantuml.com/), built on
[tree-sitter-plantuml](https://gitlab.semantiqa.dev/deriva/plantuml/tree-sitter-plantuml).
Part of the `deriva/plantuml` family: grammar → formatter → LSP → editor.

<!-- folio: colophon --project plantuml-fmt -->
![powered by: argos](https://img.shields.io/badge/powered%20by-argos-1f6feb) ![reqs verified: 100%](https://img.shields.io/badge/reqs%20verified-100%25-2ea44f)

> **plantuml-fmt** is powered by **argos**. **folio** generates this documentation from the repository's model: 10 requirements · 10 verifications · 0 constraints. Quality: 100% verified.
<!-- /folio -->

Two guarantees: **lossless** (only whitespace changes; opaque content is
preserved byte-identical) and **idempotent** (`fmt(fmt(x)) == fmt(x)`).
Every style rule is a versioned requirement with its own test.

## Install

Straight from git; pip resolves the grammar dependency itself. The block
below is generated from the manifest and the latest tag:

<!-- folio: install -->
```bash
pip install git+https://gitlab.semantiqa.dev/deriva/plantuml/plantuml-fmt.git@v0.3.2
```

Or from a clone: `git clone https://gitlab.semantiqa.dev/deriva/plantuml/plantuml-fmt && pip install ./plantuml-fmt`.
<!-- /folio -->

## Use cases

**Check a diagram tree**, in CI or locally. Reports offending files and
exits 1:

```bash
plantuml-fmt --check diagrams/
```

**Rewrite in place** to the canonical style:

```bash
plantuml-fmt --write diagrams/
```

**As a pre-commit hook**, so formatting runs before every commit:

```yaml
repos:
  - repo: https://gitlab.semantiqa.dev/deriva/plantuml/plantuml-fmt
    rev: v0.3.2
    hooks:
      - id: plantuml-fmt
```

**From your editor**: [plantuml-lsp](https://gitlab.semantiqa.dev/deriva/plantuml/plantuml-lsp)
delegates `textDocument/formatting` here, so format-on-save in Neovim
([plantuml.nvim](https://gitlab.semantiqa.dev/deriva/plantuml/plantuml.nvim)) or
VS Code produces the same bytes as the hook.

## Documentation

- [Canonical style](doc/rules.md): the formatting rules, one by one
- [Architecture](doc/architecture.md): the model's diagrams, rendered from source
- [Requirements & status](doc/requirements.md): the per-requirement board with its evidence
- [Rationale](doc/rationale.md): why the formatter is the way it is
