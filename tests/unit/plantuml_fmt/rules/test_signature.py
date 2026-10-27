"""A method's signature fields, their re-emission and their identity."""

from plantuml_fmt.rules.signature import emit_method, method_signature, signature_key
from tests.unit.plantuml_fmt.rules._tree import method_in

__covers__ = (method_signature, emit_method, signature_key)


class TestMethodSignature:
    def test_keeps_a_left_type_left(self) -> None:
        src, node = method_in(b"+int go( int a ,bool b )")
        sig = method_signature(src, node)
        assert sig["left"] == b"int" and sig["right"] is None
        assert sig["params"] == (b"int a", b"bool b")


class TestEmitMethod:
    def test_joins_parameters_and_puts_a_right_type_after_a_colon(self) -> None:
        sig = {
            "left": None,
            "right": b"int",
            "name": b"go",
            "tparams": None,
            "params": (b"a", b"b"),
            "suffix": b"const",
        }
        assert emit_method(sig) == b"go(a, b) const : int"


class TestSignatureKey:
    def test_is_blind_to_the_side_of_the_type(self) -> None:
        base = {"name": b"go", "tparams": None, "params": (), "suffix": None}
        assert signature_key({**base, "left": b"int", "right": None}) == signature_key(
            {**base, "left": None, "right": b"int"}
        )
