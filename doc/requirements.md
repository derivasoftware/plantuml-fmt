# Requirements & status

## What was asked

The system requirements, with a check for implemented (its requirements
land on diagrams that resolve to code) and one per test suite: UT and ST
say whether that suite's last run covered the requirement's verification
tests with no failures.

<!-- folio: sreqs --junit test-results/junit.xml --junit_st test-results/junit-st.xml -->
| SREQ | Title | Implemented | UT | ST |
| --- | --- | --- | --- | --- |
| `SREQ-00001-1` | The tool shall format PlantUML sources into a canonical style | ~ | ~ | ~ |
| `SREQ-00002-2` | Formatting shall never change what a diagram says | ✓ | ~ | ✓ |
| `SREQ-00003-1` | The formatter shall emit identical output when reformatting its own output | ✓ | ~ | ✓ |
| `SREQ-00004-1` | The formatter shall pass opaque content through verbatim | ✓ | ✓ | ✗ |
| `SREQ-00005-1` | The tool shall provide a command-line interface with check and write modes | ✓ | ✓ | ✗ |
| `SREQ-00006-1` | The tool shall provide a pre-commit hook | ✗ | ✓ | ✗ |
| `SREQ-00007-1` | The tool shall version its canonical style rules | ✓ | ~ | ✗ |
<!-- /folio -->

## Total traceability

One system requirement per row, joined across the V: its requirements,
the diagrams they trace to, the classes or modules on those diagrams,
how many verification test ids the unit and system runs matched, and
the verifications.

<!-- folio: matrix --junit test-results/junit.xml --junit_st test-results/junit-st.xml -->
| SREQ | Requirements | Diagrams | Classes | UT | ST | Verifications |
| --- | --- | --- | --- | --- | --- | --- |
| `SREQ-00001-1` | `REQ-00001-1`<br>`REQ-00004-1`<br>`REQ-00007-2`<br>`REQ-00008-1`<br>`REQ-00009-1`<br>`REQ-00010-1`<br>`REQ-00011-1`<br>`REQ-00012-1`<br>`REQ-00013-1`<br>`REQ-00014-1`<br>`REQ-00015-1`<br>`REQ-00016-1`<br>`REQ-00017-1`<br>`REQ-00018-1` | `CL_Attributes`<br>`CL_Blanks`<br>`CL_Blocks`<br>`CL_Direction`<br>`CL_Format`<br>`CL_Formatter`<br>`CL_Frames`<br>`CL_MemberRules`<br>`CL_Members`<br>`CL_Methods`<br>`CL_Opaque`<br>`CL_PlantumlFmt`<br>`CL_Reading`<br>`CL_Relations`<br>`CL_Rows`<br>`CL_Rules`<br>`CL_Signature`<br>`HLD_PlantumlFmt` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.formatter.blanks`<br>`plantuml_fmt.formatter.blocks`<br>`plantuml_fmt.formatter.format`<br>`plantuml_fmt.formatter.frames`<br>`plantuml_fmt.formatter.opaque`<br>`plantuml_fmt.formatter.rows`<br>`plantuml_fmt.rules`<br>`plantuml_fmt.rules.attributes`<br>`plantuml_fmt.rules.direction`<br>`plantuml_fmt.rules.members`<br>`plantuml_fmt.rules.methods`<br>`plantuml_fmt.rules.reading`<br>`plantuml_fmt.rules.relations`<br>`plantuml_fmt.rules.signature` | 70 | 0 | `VER-00001-1`<br>`VER-00004-1`<br>`VER-00007-1`<br>`VER-00008-1`<br>`VER-00009-1`<br>`VER-00010-1`<br>`VER-00011-4`<br>`VER-00012-1`<br>`VER-00013-1`<br>`VER-00014-1`<br>`VER-00015-1`<br>`VER-00016-1`<br>`VER-00017-1`<br>`VER-00018-1` |
| `SREQ-00002-2` | `REQ-00001-1`<br>`REQ-00007-2`<br>`REQ-00008-1`<br>`REQ-00009-1`<br>`REQ-00010-1`<br>`REQ-00011-1`<br>`REQ-00012-1`<br>`REQ-00014-1`<br>`REQ-00017-1`<br>`REQ-00018-1` | `CL_Attributes`<br>`CL_Blanks`<br>`CL_Blocks`<br>`CL_Direction`<br>`CL_Format`<br>`CL_Frames`<br>`CL_MemberRules`<br>`CL_Members`<br>`CL_Methods`<br>`CL_Relations`<br>`CL_Rows`<br>`CL_Signature` | `plantuml_fmt.formatter.blanks`<br>`plantuml_fmt.formatter.blocks`<br>`plantuml_fmt.formatter.format`<br>`plantuml_fmt.formatter.frames`<br>`plantuml_fmt.formatter.rows`<br>`plantuml_fmt.rules`<br>`plantuml_fmt.rules.attributes`<br>`plantuml_fmt.rules.direction`<br>`plantuml_fmt.rules.members`<br>`plantuml_fmt.rules.methods`<br>`plantuml_fmt.rules.relations`<br>`plantuml_fmt.rules.signature` | 61 | 0 | `VER-00001-1`<br>`VER-00007-1`<br>`VER-00008-1`<br>`VER-00009-1`<br>`VER-00010-1`<br>`VER-00011-4`<br>`VER-00012-1`<br>`VER-00014-1`<br>`VER-00017-1`<br>`VER-00018-1` |
| `SREQ-00003-1` | `REQ-00001-1`<br>`REQ-00007-2`<br>`REQ-00008-1`<br>`REQ-00009-1`<br>`REQ-00010-1`<br>`REQ-00011-1`<br>`REQ-00012-1`<br>`REQ-00014-1`<br>`REQ-00017-1`<br>`REQ-00018-1` | `CL_Attributes`<br>`CL_Blanks`<br>`CL_Blocks`<br>`CL_Direction`<br>`CL_Format`<br>`CL_Frames`<br>`CL_MemberRules`<br>`CL_Members`<br>`CL_Methods`<br>`CL_Relations`<br>`CL_Rows`<br>`CL_Signature` | `plantuml_fmt.formatter.blanks`<br>`plantuml_fmt.formatter.blocks`<br>`plantuml_fmt.formatter.format`<br>`plantuml_fmt.formatter.frames`<br>`plantuml_fmt.formatter.rows`<br>`plantuml_fmt.rules`<br>`plantuml_fmt.rules.attributes`<br>`plantuml_fmt.rules.direction`<br>`plantuml_fmt.rules.members`<br>`plantuml_fmt.rules.methods`<br>`plantuml_fmt.rules.relations`<br>`plantuml_fmt.rules.signature` | 61 | 0 | `VER-00001-1`<br>`VER-00007-1`<br>`VER-00008-1`<br>`VER-00009-1`<br>`VER-00010-1`<br>`VER-00011-4`<br>`VER-00012-1`<br>`VER-00014-1`<br>`VER-00017-1`<br>`VER-00018-1` |
| `SREQ-00004-1` | `REQ-00004-1` | `CL_Opaque` | `plantuml_fmt.formatter.opaque` | 4 | 0 | `VER-00004-1` |
| `SREQ-00005-1` | `REQ-00005-1` | `CL_Cli` | `plantuml_fmt.cli` | 2 | 0 | `VER-00005-1` |
| `SREQ-00006-1` | `REQ-00006-1` | — | — | 1 | 0 | `VER-00006-1` |
| `SREQ-00007-1` | `REQ-00001-1`<br>`REQ-00007-2`<br>`REQ-00008-1`<br>`REQ-00009-1`<br>`REQ-00011-1`<br>`REQ-00012-1`<br>`REQ-00017-1`<br>`REQ-00018-1` | `CL_Attributes`<br>`CL_Blocks`<br>`CL_Direction`<br>`CL_Frames`<br>`CL_MemberRules`<br>`CL_Members`<br>`CL_Methods`<br>`CL_Relations`<br>`CL_Signature` | `plantuml_fmt.formatter.blocks`<br>`plantuml_fmt.formatter.frames`<br>`plantuml_fmt.rules`<br>`plantuml_fmt.rules.attributes`<br>`plantuml_fmt.rules.direction`<br>`plantuml_fmt.rules.members`<br>`plantuml_fmt.rules.methods`<br>`plantuml_fmt.rules.relations`<br>`plantuml_fmt.rules.signature` | 41 | 0 | `VER-00001-1`<br>`VER-00007-1`<br>`VER-00008-1`<br>`VER-00009-1`<br>`VER-00011-4`<br>`VER-00012-1`<br>`VER-00017-1`<br>`VER-00018-1` |
<!-- /folio -->
