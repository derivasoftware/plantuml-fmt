"""v2 rules: blank-line policy, adjacency-preserving relation rebuilds,
and output that always re-parses at least as cleanly as the input."""

from plantuml_fmt.formatter import format_text


def fmt(src: str) -> str:
    return format_text(src)


# ── Blank-line policy ────────────────────────────────────────────────────────

def test_collapses_blank_runs_to_one():
    src = "@startuml\nclass A\n\n\n\nclass B\n@enduml\n"
    assert fmt(src) == "@startuml\nclass A\n\nclass B\n@enduml\n"


def test_strips_blanks_at_block_edges():
    src = "@startuml\nclass A {\n\n  +x : int\n\n}\n@enduml\n"
    assert fmt(src) == "@startuml\nclass A {\n  + x : int\n}\n@enduml\n"


def test_strips_blanks_at_frame_edges():
    src = "@startuml\nalt ok\n\n  a -> b\n\nelse ko\n\n  a -> c\n\nend\n@enduml\n"
    assert fmt(src) == (
        "@startuml\nalt ok\n  a -> b\nelse ko\n  a -> c\nend\n@enduml\n"
    )


def test_keeps_single_blank_between_top_level_statements():
    src = "@startuml\nclass A\n\nclass B\n@enduml\n"
    assert fmt(src) == src


def test_note_bodies_keep_their_blank_lines():
    src = "@startuml\nnote as N\nline one\n\nline two\nend note\n@enduml\n"
    assert fmt(src) == src


# ── Adjacency-preserving rebuilds ────────────────────────────────────────────

def test_role_slash_cardinalities_stay_glued():
    src = '@startuml\nUser   "owner"/1   --   "0..n"/items   Item\n@enduml\n'
    assert fmt(src) == '@startuml\nUser "owner"/1 -- "0..n"/items Item\n@enduml\n'


def test_activation_shorthand_spacing():
    src = "@startuml\nAlice   ->   Bob   ++   #gold   :   go\n@enduml\n"
    assert fmt(src) == "@startuml\nAlice -> Bob ++ #gold : go\n@enduml\n"


def test_boundary_messages_normalize():
    src = "@startuml\n[->   Bob   :   hello\nBob   ->]   :   bye\n@enduml\n"
    assert fmt(src) == "@startuml\n[-> Bob : hello\nBob ->] : bye\n@enduml\n"


# ── Round-trip safety ────────────────────────────────────────────────────────

def test_formatted_output_is_idempotent_and_lossless():
    src = (
        "@startuml\n"
        'participant "Front End" as FE << (C,#ADD1B2) UI >>\n'
        "\n\n"
        "User -> FE ++ : click\n"
        "FE --> User -- : ack\n"
        'Shop [customerId] ---> "1" Customer\n'
        "alt cached\n\n  FE -> FE : hit\n\nend\n"
        "@enduml\n"
    )
    once = fmt(src)
    assert fmt(once) == once
    strip = lambda s: "".join(s.split())
    assert strip(once) == strip(src)
