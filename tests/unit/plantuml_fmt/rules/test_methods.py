"""A method rebuilt in its written direction unless a style moves it."""

from plantuml_fmt.rules.methods import rewrite_method
from tests.unit.plantuml_fmt.rules._tree import method_in

__covers__ = (rewrite_method,)


class TestRewriteMethod:
    def test_keeps_the_written_direction_by_default(self) -> None:
        src, node = method_in(b"+int  go(int a)")
        assert rewrite_method(src, node) == b"int go(int a)"

    def test_a_requested_style_moves_the_type(self) -> None:
        src, node = method_in(b"+int go(int a)")
        assert rewrite_method(src, node, "canonical") == b"go(int a) : int"
