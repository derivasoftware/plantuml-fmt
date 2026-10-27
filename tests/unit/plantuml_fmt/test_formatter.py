"""The formatter's surface: bytes in, bytes out, whitespace only."""

import pytest

from plantuml_fmt.formatter import format_bytes, format_text

__covers__ = (format_bytes, format_text)


class TestFormatBytes:
    def test_indents_a_block_body_two_spaces(self) -> None:
        assert (
            format_bytes(b"@startuml\nclass A {\n+x : int\n}\n@enduml\n")
            == b"@startuml\nclass A {\n  + x : int\n}\n@enduml\n"
        )

    def test_collapses_a_run_of_blank_lines_to_one(self) -> None:
        assert (
            format_bytes(b"@startuml\nclass A\n\n\n\nclass B\n@enduml\n")
            == b"@startuml\nclass A\n\nclass B\n@enduml\n"
        )

    def test_keeps_a_note_body_byte_identical(self) -> None:
        src = b"@startuml\nnote as N\n    free   text\nend note\n@enduml\n"
        assert format_bytes(src) == src

    def test_reaches_a_fixed_point_in_one_pass(self) -> None:
        once = format_bytes(
            b"@startuml\nnamespace n {\nclass A {\n+go( a ,b ) : int\n}\n}\nA-->B\n@enduml\n"
        )
        assert format_bytes(once) == once

    def test_rejects_an_unknown_member_style(self) -> None:
        with pytest.raises(ValueError):
            format_bytes(b"@startuml\n@enduml\n", "sideways")


class TestFormatText:
    def test_is_format_bytes_over_text(self) -> None:
        assert (
            format_text("@startuml\nA   -->   B\n@enduml\n")
            == "@startuml\nA --> B\n@enduml\n"
        )

    def test_glued_tokens_stay_glued(self) -> None:
        assert (
            format_text("@startuml\nA-->B\n@enduml\n") == "@startuml\nA-->B\n@enduml\n"
        )
