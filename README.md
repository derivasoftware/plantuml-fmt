# plantuml-fmt

<!-- folio: colophon --project plantuml-fmt --junit test-results/junit.xml --junit_st test-results/junit-st.xml --coverage_ut test-results/coverage-ut.xml --coverage_st test-results/coverage-st.xml -->
![powered by: argos](https://img.shields.io/badge/powered%20by-argos-1f6feb) ![traced: 94%](https://img.shields.io/badge/traced-94%25-2ea44f) ![verified: 100%](https://img.shields.io/badge/verified-100%25-2ea44f) ![tests: 100%](https://img.shields.io/badge/tests-100%25-2ea44f) ![UT: 97%](https://img.shields.io/badge/UT-97%25-2ea44f) ![ST: 79%](https://img.shields.io/badge/ST-79%25-dfb317) ![diagnostics: 0](https://img.shields.io/badge/diagnostics-0-2ea44f)

> **plantuml-fmt** is powered by **argos**. **folio** generates this documentation from the repository's model: 16 requirements · 16 verifications · 2 constraints. Quality: 94% traced to code · 100% verified · 100% tests passing · 97% UT coverage · 79% ST coverage.
<!-- /folio -->

Canonical formatter for [PlantUML](https://plantuml.com/), built on
[tree-sitter-plantuml](https://github.com/derivasoftware/tree-sitter-plantuml).
Part of the `deriva/plantuml` family: grammar → formatter → LSP → editor.

Two guarantees: **lossless** (only whitespace changes; opaque content is
preserved byte-identical, and a line a rewrite cannot rebuild whole keeps
its bytes) and **idempotent** (`fmt(fmt(x)) == fmt(x)`). Every style rule
is a versioned requirement with its own test; the two guarantees are the
constraints every rule obeys.

## Install

Straight from git; pip resolves the grammar dependency itself. The block
below is generated from the manifest and the latest tag:

<!-- folio: install -->
```bash
pip install git+https://github.com/derivasoftware/plantuml-fmt.git@v0.6.2
```

Or from a clone: `git clone https://github.com/derivasoftware/plantuml-fmt && pip install ./plantuml-fmt`.
<!-- /folio -->

## Use cases

**Check a diagram tree**, in CI or locally. Reports offending files and
exits 1:

```bash
plantuml-fmt --check diagrams/
```

**Rewrite in place** to the canonical style (the default mode):

```bash
plantuml-fmt diagrams/
```

**Convert method direction**, on request only: `--member-style canonical`
writes `name(args) : type`, `--member-style cpp` writes `type name(args)`;
a conversion stands only when the converted line re-parses to the same
signature. The default, `preserve`, keeps the direction as written.

**As a pre-commit hook**, so formatting runs before every commit:

```yaml
repos:
  - repo: https://github.com/derivasoftware/plantuml-fmt
    rev: v0.6.1
    hooks:
      - id: plantuml-fmt
```

**From your editor**: [plantuml-lsp](https://github.com/derivasoftware/plantuml-lsp)
delegates `textDocument/formatting` here, so format-on-save in Neovim
([plantuml.nvim](https://github.com/derivasoftware/plantuml.nvim)) or
VS Code produces the same bytes as the hook.

## Scope

The family covers a standard-driven subset of PlantUML, never the whole
language. Class diagrams: 125 of 149 standard constructs structural;
sequence: participants, arrows, frames, notes and the lifecycle verbs
(activate, create, destroy, return, ref, box, delays, spacers)
structural, with autonumber, autoactivate and the styling surface raw;
activity: actions, swimlanes and the whole new-syntax control flow
structural, with the legacy syntax and the braced drawing blocks raw;
state: declarations, descriptions and the composite block structural,
with concurrent regions raw. Everything else (deployment, components,
mindmaps, gantt) parses lossless as raw lines, never an ERROR, but gets
no structure. The formatter normalizes what the grammar structures
and preserves the rest byte-identical.

## Documentation

- [Canonical style](doc/rules.md): the formatting rules, one by one
- [Architecture](doc/architecture.md): the model's diagrams, rendered from source
- [Requirements & status](doc/requirements.md): what was asked and the traceability matrix
- [Repo quality](doc/quality.md): artefact inventory and health metrics

*Not affiliated with or endorsed by the PlantUML project.*
