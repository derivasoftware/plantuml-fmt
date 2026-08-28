# Requirements & status

## What was asked

The system requirements, with a check for implemented (its requirements
land on diagrams that resolve to code) and one per test suite: UT and ST
say whether that suite's last run covered the requirement's verification
tests with no failures.

<!-- folio: sreqs --junit test-results/junit.xml --junit_st test-results/junit-st.xml -->
| SREQ | Title | Implemented | UT | ST |
| --- | --- | --- | --- | --- |
| `SREQ-00001-1` | The tool shall format PlantUML sources into a canonical style | ✓ | ✓ | ~ |
| `SREQ-00002-1` | The formatter shall preserve every input token byte-identically | ✓ | ✓ | ✓ |
| `SREQ-00003-1` | The formatter shall emit identical output when reformatting its own output | ✓ | ✓ | ✓ |
| `SREQ-00004-1` | The formatter shall pass opaque content through verbatim | ✓ | ✓ | ✗ |
| `SREQ-00005-1` | The tool shall provide a command-line interface with check and write modes | ✓ | ✓ | ✗ |
| `SREQ-00006-1` | The tool shall provide a pre-commit hook | ✓ | ✓ | ✗ |
| `SREQ-00007-1` | The tool shall version its canonical style rules | ✓ | ✓ | ✗ |
<!-- /folio -->

## Total traceability

One system requirement per row, joined across the V: its requirements,
the diagrams they trace to, the classes or modules on those diagrams,
how many verification test ids the unit and system runs matched, and
the verifications.

<!-- folio: matrix --junit test-results/junit.xml --junit_st test-results/junit-st.xml -->
| SREQ | Requirements | Diagrams | Classes | UT | ST | Verifications |
| --- | --- | --- | --- | --- | --- | --- |
| `SREQ-00001-1` | `REQ-00001-1`<br>`REQ-00007-2`<br>`REQ-00008-1`<br>`REQ-00009-1`<br>`REQ-00010-1`<br>`REQ-00011-1` | `CL_Formatter`<br>`CL_PlantumlFmt`<br>`CL_Rules`<br>`HLD_PlantumlFmt` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.rules` | 25 | 0 | `VER-00001-1`<br>`VER-00007-1`<br>`VER-00008-1`<br>`VER-00009-1`<br>`VER-00010-1`<br>`VER-00011-3` |
| `SREQ-00002-1` | `REQ-00003-4` | `CL_Formatter`<br>`CL_PlantumlFmt`<br>`CL_Rules` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.rules` | 1 | 1 | `VER-00003-3` |
| `SREQ-00003-1` | `REQ-00002-1` | `CL_Formatter`<br>`CL_PlantumlFmt` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.rules` | 1 | 1 | `VER-00002-2` |
| `SREQ-00004-1` | `REQ-00004-1` | `CL_Formatter`<br>`CL_PlantumlFmt` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.rules` | 3 | 0 | `VER-00004-1` |
| `SREQ-00005-1` | `REQ-00005-1` | `CL_Cli`<br>`CL_PlantumlFmt` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.rules` | 1 | 0 | `VER-00005-1` |
| `SREQ-00006-1` | `REQ-00006-1` | `CL_Cli`<br>`CL_PlantumlFmt` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.rules` | 1 | 0 | `VER-00006-1` |
| `SREQ-00007-1` | `REQ-00001-1`<br>`REQ-00007-2`<br>`REQ-00008-1`<br>`REQ-00009-1` | `CL_Formatter`<br>`CL_PlantumlFmt`<br>`CL_Rules` | `plantuml_fmt.cli`<br>`plantuml_fmt.formatter`<br>`plantuml_fmt.rules` | 7 | 0 | `VER-00001-1`<br>`VER-00007-1`<br>`VER-00008-1`<br>`VER-00009-1` |
<!-- /folio -->
