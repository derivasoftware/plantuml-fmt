# Architecture

The formatter is three pieces: the CLI walks files, the Formatter decides
which lines it may touch (freezing opaque content), and the Rules rewrite
relations and members token by token. The figures below are the repository's
actual design, rendered from its sources on every inject.

<!-- folio: design --assets assets -->
### System view

#### HLD_PlantumlFmt

_hld · `design/hld/HLD_PlantumlFmt.puml`_ (traces to SREQ-00001-1)

![HLD_PlantumlFmt](assets/HLD_PlantumlFmt.svg)

### Module overview

#### CL_PlantumlFmt

_cl · `design/lld/plantuml_fmt/CL_PlantumlFmt.puml`_ (traces to REQ-00001-1, REQ-00002-1, REQ-00003-4, REQ-00004-1, REQ-00005-1, REQ-00006-1, REQ-00007-2, REQ-00008-1, REQ-00009-1)

implemented in `src/plantuml_fmt/cli.py`, `src/plantuml_fmt/formatter.py`, `src/plantuml_fmt/rules.py` · verified by `tests/test_cli.py` (1), `tests/test_formatter.py` (9), `tests/test_hooks.py` (1), `tests/test_v2.py` (3)

![CL_PlantumlFmt](assets/CL_PlantumlFmt.svg)

### Class detail

<details>
<summary><code>CL_Formatter</code> · traces to <code>REQ-00001-1</code> <code>REQ-00002-1</code> <code>REQ-00003-4</code> <code>REQ-00004-1</code> <code>REQ-00009-1</code> <code>REQ-00010-1</code></summary>
<p><code>design/lld/plantuml_fmt/CL_Formatter.puml</code></p>
<p><img alt="CL_Formatter" src="assets/CL_Formatter.svg"></p>
</details>

<details>
<summary><code>CL_Rules</code> · traces to <code>REQ-00003-4</code> <code>REQ-00007-2</code> <code>REQ-00008-1</code></summary>
<p><code>design/lld/plantuml_fmt/CL_Rules.puml</code></p>
<p><img alt="CL_Rules" src="assets/CL_Rules.svg"></p>
</details>

<details>
<summary><code>CL_Cli</code> · traces to <code>REQ-00005-1</code> <code>REQ-00006-1</code></summary>
<p><code>design/lld/plantuml_fmt/CL_Cli.puml</code></p>
<p><img alt="CL_Cli" src="assets/CL_Cli.svg"></p>
</details>
<!-- /folio -->
