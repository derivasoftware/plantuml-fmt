# Architecture

The formatter is three pieces: the CLI walks files, the Formatter decides
which lines it may touch (freezing opaque content), and the Rules rewrite
relations and members token by token. The figures below are the repository's
actual design, rendered from its sources on every inject.

<!-- folio: design --assets assets -->
### System view

#### HLD_PlantumlFmt

_hld · `design/hld/HLD_PlantumlFmt.puml`_

- traces to: `SREQ-00001-1`

![HLD_PlantumlFmt](assets/HLD_PlantumlFmt.svg)

### Module overview

#### CL_Cli

_cl · `design/lld/plantuml_fmt/CL_Cli.puml`_

- traces to: `REQ-00005-1` `REQ-00006-1`
- implemented in: `src/plantuml_fmt/cli.py`
- verified by: `tests/integration/test_cli.py` (1) · `tests/integration/test_hooks.py` (1)

![CL_Cli](assets/CL_Cli.svg)

#### CL_Formatter

_cl · `design/lld/plantuml_fmt/CL_Formatter.puml`_

- traces to: `REQ-00001-1` `REQ-00004-1` `REQ-00009-1` `REQ-00010-1`
- implemented in: `src/plantuml_fmt/formatter.py`
- verified by: `tests/integration/test_formatter.py` (5) · `tests/integration/test_it_v2.py` (5)

![CL_Formatter](assets/CL_Formatter.svg)

#### CL_PlantumlFmt

_cl · `design/lld/plantuml_fmt/CL_PlantumlFmt.puml`_

- traces to: `REQ-00001-1` `REQ-00004-1` `REQ-00005-1` `REQ-00006-1` `REQ-00007-2` `REQ-00008-1` `REQ-00009-1` `REQ-00012-1`
- implemented in: `src/plantuml_fmt/cli.py` · `src/plantuml_fmt/formatter.py` · `src/plantuml_fmt/rules.py`
- verified by: `tests/integration/test_cli.py` (2) · `tests/integration/test_formatter.py` (7) · `tests/integration/test_hooks.py` (1) · `tests/integration/test_it_v2.py` (3) · `tests/integration/test_member_style.py` (12)

![CL_PlantumlFmt](assets/CL_PlantumlFmt.svg)

### Class detail

<details>
<summary><code>CL_Rules</code> · traces to <code>REQ-00007-2</code> <code>REQ-00008-1</code> <code>REQ-00011-1</code> <code>REQ-00012-1</code></summary>
<ul>
<li>source: <code>design/lld/plantuml_fmt/CL_Rules.puml</code></li>
<li>implemented in: <code>src/plantuml_fmt/rules.py</code></li>
<li>verified by: <code>tests/integration/test_cli.py</code> (1), <code>tests/integration/test_cpp_members.py</code> (15), <code>tests/integration/test_formatter.py</code> (2), <code>tests/integration/test_it_v2.py</code> (3), <code>tests/integration/test_member_style.py</code> (12)</li>
</ul>
<p><img alt="CL_Rules" src="assets/CL_Rules.svg"></p>
</details>
<!-- /folio -->
