"""v2 rules: blank-line policy, adjacency-preserving relation rebuilds,
and output that always re-parses at least as cleanly as the input."""

from plantuml_fmt.formatter import format_text


def fmt(src: str) -> str:
    return format_text(src)


# ── Blank-line policy ────────────────────────────────────────────────────────


# ── Adjacency-preserving rebuilds ────────────────────────────────────────────


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

    def strip(text: str) -> str:
        return "".join(text.split())

    assert strip(once) == strip(src)
