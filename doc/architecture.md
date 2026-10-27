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

#### CL_Attributes

_cl · `design/lld/plantuml_fmt/rules/CL_Attributes.puml`_

- traces to: `REQ-00017-1`
- implemented in: `src/plantuml_fmt/rules/attributes.py`
- verified by: `tests/integration/rules/test_attributes.py` (3)

![CL_Attributes](assets/CL_Attributes.svg)

#### CL_Blocks

_cl · `design/lld/plantuml_fmt/formatter/CL_Blocks.puml`_

- traces to: `REQ-00001-1`
- implemented in: `src/plantuml_fmt/formatter/blocks.py`
- verified by: `tests/integration/formatter/test_blocks.py` (2)

![CL_Blocks](assets/CL_Blocks.svg)

#### CL_Cli

_cl · `design/lld/plantuml_fmt/CL_Cli.puml`_

- traces to: `REQ-00005-1`
- implemented in: `src/plantuml_fmt/cli.py`
- verified by: `tests/integration/test_cli.py` (2)

![CL_Cli](assets/CL_Cli.svg)

#### CL_Direction

_cl · `design/lld/plantuml_fmt/rules/CL_Direction.puml`_

- traces to: `REQ-00012-1`
- implemented in: `src/plantuml_fmt/rules/direction.py`
- verified by: `tests/integration/test_member_style.py` (9)

![CL_Direction](assets/CL_Direction.svg)

#### CL_Format

_cl · `design/lld/plantuml_fmt/formatter/CL_Format.puml`_

- traces to: `REQ-00014-1`
- implemented in: `src/plantuml_fmt/formatter/format.py`
- verified by: `tests/integration/test_formatter.py` (8) · `tests/integration/test_it_v2.py` (8)

![CL_Format](assets/CL_Format.svg)

#### CL_Formatter

_cl · `design/lld/plantuml_fmt/formatter/CL_Formatter.puml`_

- traces to: `REQ-00013-1`

![CL_Formatter](assets/CL_Formatter.svg)

#### CL_Frames

_cl · `design/lld/plantuml_fmt/formatter/CL_Frames.puml`_

- traces to: `REQ-00009-1`
- implemented in: `src/plantuml_fmt/formatter/frames.py`
- verified by: `tests/integration/formatter/test_frames.py` (4)

![CL_Frames](assets/CL_Frames.svg)

#### CL_MemberRules

_cl · `design/lld/plantuml_fmt/rules/CL_MemberRules.puml`_

- traces to: `REQ-00008-1`

![CL_MemberRules](assets/CL_MemberRules.svg)

#### CL_Members

_cl · `design/lld/plantuml_fmt/rules/CL_Members.puml`_

- traces to: `REQ-00018-1`
- implemented in: `src/plantuml_fmt/rules/members.py`
- verified by: `tests/integration/rules/test_members.py` (4)

![CL_Members](assets/CL_Members.svg)

#### CL_Methods

_cl · `design/lld/plantuml_fmt/rules/CL_Methods.puml`_

- traces to: `REQ-00011-1`
- implemented in: `src/plantuml_fmt/rules/methods.py`
- verified by: `tests/integration/test_cpp_members.py` (15)

![CL_Methods](assets/CL_Methods.svg)

#### CL_Opaque

_cl · `design/lld/plantuml_fmt/formatter/CL_Opaque.puml`_

- traces to: `REQ-00004-1`
- implemented in: `src/plantuml_fmt/formatter/opaque.py`
- verified by: `tests/integration/formatter/test_opaque.py` (4)

![CL_Opaque](assets/CL_Opaque.svg)

#### CL_PlantumlFmt

_cl · `design/lld/plantuml_fmt/CL_PlantumlFmt.puml`_

- traces to: `SREQ-00001-1`
- implemented in: `src/plantuml_fmt/cli.py`

![CL_PlantumlFmt](assets/CL_PlantumlFmt.svg)

#### CL_Relations

_cl · `design/lld/plantuml_fmt/rules/CL_Relations.puml`_

- traces to: `REQ-00007-2`
- implemented in: `src/plantuml_fmt/rules/relations.py`
- verified by: `tests/integration/rules/test_relations.py` (4)

![CL_Relations](assets/CL_Relations.svg)

#### CL_Rules

_cl · `design/lld/plantuml_fmt/rules/CL_Rules.puml`_

- traces to: `REQ-00015-1`

![CL_Rules](assets/CL_Rules.svg)

#### CL_Signature

_cl · `design/lld/plantuml_fmt/rules/CL_Signature.puml`_

- traces to: `REQ-00011-1`
- implemented in: `src/plantuml_fmt/rules/signature.py`
- verified by: `tests/integration/test_cpp_members.py` (15)

![CL_Signature](assets/CL_Signature.svg)

### Class detail

<details>
<summary><code>CL_Blanks</code> · traces to <code>REQ-00010-1</code></summary>
<ul>
<li>source: <code>design/lld/plantuml_fmt/formatter/CL_Blanks.puml</code></li>
<li>implemented in: <code>src/plantuml_fmt/formatter/blanks.py</code></li>
<li>verified by: <code>tests/integration/formatter/test_blanks.py</code> (4)</li>
</ul>
<p><img alt="CL_Blanks" src="assets/CL_Blanks.svg"></p>
</details>

<details>
<summary><code>CL_Reading</code> · traces to <code>REQ-00016-1</code></summary>
<ul>
<li>source: <code>design/lld/plantuml_fmt/rules/CL_Reading.puml</code></li>
<li>implemented in: <code>src/plantuml_fmt/rules/reading.py</code></li>
<li>verified by: <code>tests/integration/rules/test_reading.py</code> (5)</li>
</ul>
<p><img alt="CL_Reading" src="assets/CL_Reading.svg"></p>
</details>

<details>
<summary><code>CL_Rows</code> · traces to <code>REQ-00014-1</code></summary>
<ul>
<li>source: <code>design/lld/plantuml_fmt/formatter/CL_Rows.puml</code></li>
<li>implemented in: <code>src/plantuml_fmt/formatter/rows.py</code></li>
<li>verified by: <code>tests/integration/test_formatter.py</code> (8), <code>tests/integration/test_it_v2.py</code> (8)</li>
</ul>
<p><img alt="CL_Rows" src="assets/CL_Rows.svg"></p>
</details>
<!-- /folio -->
