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
