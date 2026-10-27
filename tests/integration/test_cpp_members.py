"""C++ member signatures keep their shape through the formatter
(REQ-00011-1): the left return type stays left, trailing qualifiers
keep single spacing, the cv-qualifier stays between the parens and the
canonical colon, and a callable parameter's inner parentheses never
split the list. Malformed C++ falls through untouched — lossless.

The tests drive the method rewrite itself (rules.methods) over a parsed
class body; the member's visibility is carried over as written."""

from plantuml_fmt.rules.methods import rewrite_method
from tests.integration._grammar import parse


def _rewrite(line: str) -> str:
    src = f"@startuml\nclass C {{\n  {line}\n}}\n@enduml\n".encode()
    stack = [parse(src).root_node]
    while stack:
        node = stack.pop()
        if node.type == "method":
            out = rewrite_method(src, node)
            if out is None:
                return line
            line_start = src.rfind(b"\n", 0, node.start_byte) + 1
            head = b" ".join(src[line_start : node.start_byte].split())
            return ((head + b" ") if head else b"").decode() + out.decode()
        stack.extend(node.children)
    return line  # the grammar left it raw: nothing to rewrite


def _member(line: str) -> str:
    out = _rewrite(line)
    assert _rewrite(out) == out, "idempotency"
    return out


def test_left_return_type_is_preserved():
    assert _member("+ std::string get_name()") == "+ std::string get_name()"


def test_nested_template_return_survives_whole():
    line = "+ std::map<std::string, std::vector<int>> table()"
    assert _member(line) == line


def test_deleted_assignment_keeps_form_and_spacing():
    assert (
        _member("+ ThreadPool& operator=(const ThreadPool&) =  delete")
        == "+ ThreadPool& operator=(const ThreadPool&) = delete"
    )


def test_cv_qualifier_sits_before_the_canonical_colon():
    assert (
        _member("+ worker_count() const : std::size_t")
        == "+ worker_count() const : std::size_t"
    )


def test_callable_parameter_inner_parens_do_not_split():
    line = "+ submit(task : std::function<void(int, bool)>) : void"
    assert _member(line) == line


def test_canonical_colon_form_still_normalizes():
    assert _member("+ get_name(): std::string") == "+ get_name() : std::string"


def test_unclosed_template_falls_through_lossless():
    line = "+ std::map<std::string broken()"
    out = _member(line)
    assert "".join(out.split()) == "".join(line.split())


# Method-level template parameters (grammar 0.9.5, tree-sitter-plantuml#5):
# the clause between the name and the parenthesis is a token like any
# other — it survives, in both directions, and the line stays idempotent.
def test_template_clause_survives_behind_cpp_return_type():
    line = "+ Widget* create<Args>(Config config)"
    assert _member(line) == line


def test_template_clause_survives_behind_plain_type():
    assert _member("+ T get<T>(int index)") == "+ T get<T>(int index)"
    assert _member("+ void add<T>(T item)") == "+ void add<T>(T item)"


def test_template_clause_survives_in_canonical_colon_form():
    assert _member("+ get<T>(int index) : T") == "+ get<T>(int index) : T"


def test_template_clause_with_nested_return_and_qualifier():
    # grammar 0.9.6 (#6): the template comma inside a parameter no longer
    # splits it, so the parameter text is kept verbatim, spacing included
    line = "+ std::vector<int> pick<K, V>(const Map<K,V>& m) const"
    assert _member(line) == line


def test_template_commas_keep_one_parameter():
    line = "+ lookup(std::map<K, std::vector<int>> m, std::pair<A, B> p) : int"
    assert _member(line) == line


def test_empty_template_clause_falls_through_lossless():
    assert _member("+ T get<>(int index)") == "+ T get<>(int index)"


# Grammar 0.9.7 (tree-sitter-plantuml#7): a plain identifier type binds
# the method path even without a template clause — its direction is
# preserved like any C++ signature, and a degenerate line carrying a
# type on each side of the name loses neither.
def test_plain_return_type_stays_left():
    assert _member("+ void start()") == "+ void start()"


def test_both_directions_on_one_line_lose_nothing():
    assert _member("+ void f() : int") == "+ void f() : int"
