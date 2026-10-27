"""The two invariants (SREQ-00002-2, SREQ-00003-1) over the golden diagram.

The corpus pass proves them over a real tree; these pin them on the one
input that exercises every rule at once, so a regression names its rule.
"""

import pytest

from plantuml_fmt.formatter import format_text
from tests.integration.test_formatter import MESSY


@pytest.mark.system
def test_idempotent():
    once = format_text(MESSY)
    assert format_text(once) == once


@pytest.mark.system
def test_only_whitespace_changes():
    def squash(text):
        return [line.replace(" ", "").replace("\t", "") for line in text.split("\n")]

    assert squash(MESSY) == squash(format_text(MESSY))


@pytest.mark.system
def test_a_line_the_rewrite_does_not_cover_keeps_its_bytes():
    # grammar 0.12+ stops a label before a brace that ends its line, leaving
    # the brace as raw text behind the relation; the line must survive whole
    src = "@startuml\nargos_toml  -->  readers : {python: [src]}\n@enduml\n"
    out = format_text(src)
    assert out.split() == src.split()
    assert format_text(out) == out
