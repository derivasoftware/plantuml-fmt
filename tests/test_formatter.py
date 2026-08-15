"""Golden, idempotency, losslessness and opaque-content tests."""

from plantuml_fmt.formatter import format_text

MESSY = """\
@startuml
    title My diagram
namespace core {
class Kernel {
        + boot() : void
      - flag : bool
}
      class Aux
}
   note right of Kernel
      keep this   exact
   body indentation
   end note
/' block
      comment continuation '/
    Dog --|> Animal
skinparam class {
   BackgroundColor White
}
@enduml
"""

EXPECTED = """\
@startuml
title My diagram
namespace core {
  class Kernel {
    + boot() : void
    - flag : bool
  }
  class Aux
}
note right of Kernel
      keep this   exact
   body indentation
end note
/' block
      comment continuation '/
Dog --|> Animal
skinparam class {
   BackgroundColor White
}
@enduml
"""


def test_golden():
    assert format_text(MESSY) == EXPECTED


def test_idempotent():
    once = format_text(MESSY)
    assert format_text(once) == once


def test_only_leading_whitespace_changes():
    before = [line.lstrip(" \t") for line in MESSY.split("\n")]
    after = [line.lstrip(" \t") for line in format_text(MESSY).split("\n")]
    assert before == after


def test_note_body_untouched():
    out = format_text(MESSY)
    assert "      keep this   exact\n" in out
    assert "   body indentation\n" in out


def test_raw_block_body_untouched():
    out = format_text(MESSY)
    assert "   BackgroundColor White\n" in out


def test_block_comment_continuation_untouched():
    out = format_text(MESSY)
    assert "      comment continuation '/" in out
