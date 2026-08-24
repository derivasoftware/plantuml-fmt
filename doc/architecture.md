# Architecture

The formatter is three pieces: the CLI walks files, the Formatter decides
which lines it may touch (freezing opaque content), and the Rules rewrite
relations and members token by token. The figures below are the repository's
actual design, rendered from its sources on every inject.

<!-- folio: design --assets assets -->
### CL_Cli

_cl · `design/lld/plantuml_fmt/CL_Cli.puml`_ (traces to REQ-00005-1, REQ-00006-1)

![CL_Cli](assets/CL_Cli.svg)

### CL_Formatter

_cl · `design/lld/plantuml_fmt/CL_Formatter.puml`_ (traces to REQ-00001-1, REQ-00002-1, REQ-00003-3, REQ-00004-1, REQ-00009-1, REQ-00010-1)

![CL_Formatter](assets/CL_Formatter.svg)

### CL_PlantumlFmt

_cl · `design/lld/plantuml_fmt/CL_PlantumlFmt.puml`_ (traces to REQ-00001-1, REQ-00002-1, REQ-00003-3, REQ-00004-1, REQ-00005-1, REQ-00006-1, REQ-00007-2, REQ-00008-1, REQ-00009-1)

![CL_PlantumlFmt](assets/CL_PlantumlFmt.svg)

### CL_Rules

_cl · `design/lld/plantuml_fmt/CL_Rules.puml`_ (traces to REQ-00003-3, REQ-00007-2, REQ-00008-1)

![CL_Rules](assets/CL_Rules.svg)

### HLD_PlantumlFmt

_hld · `design/hld/HLD_PlantumlFmt.puml`_ (traces to SREQ-00001-1)

![HLD_PlantumlFmt](assets/HLD_PlantumlFmt.svg)
<!-- /folio -->
