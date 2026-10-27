"""The requested direction, and the re-parse guard that lets it stand."""

from plantuml_fmt.rules.direction import convert, converts_faithfully
from plantuml_fmt.rules.signature import method_signature, signature_key
from tests.unit.plantuml_fmt.rules._tree import method_in

__covers__ = (convert, converts_faithfully)


class TestConvert:
    def test_canonical_moves_a_left_type_right(self) -> None:
        src, node = method_in(b"+ void start()")
        assert convert(method_signature(src, node), "canonical") == b"start() : void"

    def test_preserve_asks_for_no_move(self) -> None:
        src, node = method_in(b"+ void start()")
        assert convert(method_signature(src, node), "preserve") is None


class TestConvertsFaithfully:
    def test_accepts_a_candidate_with_the_same_signature(self) -> None:
        src, node = method_in(b"+ void start()")
        assert converts_faithfully(
            b"start() : void", signature_key(method_signature(src, node))
        )

    def test_rejects_a_candidate_that_does_not_reparse(self) -> None:
        src, node = method_in(b"+ names() : Sequence[str]")
        assert not converts_faithfully(
            b"Sequence[str] names()", signature_key(method_signature(src, node))
        )
