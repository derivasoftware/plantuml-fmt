"""Golden and opaque-content tests."""

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
    Dog   --|>   Animal:barks
alt cached
        cli   ->   repo:load
else
      cli  -->  user : ask
end
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
Dog --|> Animal : barks
alt cached
  cli -> repo : load
else
  cli --> user : ask
end
skinparam class {
   BackgroundColor White
}
@enduml
"""


def test_golden():
    assert format_text(MESSY) == EXPECTED


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


MEMBER_MESSY = """\
@startuml
class Acc {
  +   deposit( amount : int ,  ledger )  :  void
  -balance:int
}
@enduml
"""


def test_member_spacing_normalizes():
    out = format_text(MEMBER_MESSY)
    assert "  + deposit(amount : int, ledger) : void\n" in out
    assert "  - balance : int\n" in out


def test_block_bodies_indent_two_spaces_per_level():
    src = "@startuml\nnamespace n {\nclass A {\n+x : int\n}\n}\n@enduml\n"
    out = format_text(src)
    assert "namespace n {\n  class A {\n    + x : int\n  }\n}\n" in out


def test_frame_bodies_indent():
    src = "@startuml\nloop each\ncli -> repo\nend\n@enduml\n"
    out = format_text(src)
    assert "loop each\n  cli -> repo\nend\n" in out


def test_relation_spacing_normalizes():
    src = "@startuml\nDog   --|>   Animal:barks\nA -->B\n@enduml\n"
    out = format_text(src)
    assert "Dog --|> Animal : barks\n" in out
    assert "A --> B\n" in out
