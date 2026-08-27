"""C++ member signatures keep their shape through the formatter
(REQ-00011-1): the left return type stays left, trailing qualifiers
keep single spacing, the cv-qualifier stays between the parens and the
canonical colon, and a callable parameter's inner parentheses never
split the list. Malformed C++ falls through untouched — lossless."""

import pytest

from plantuml_fmt.formatter import format_text


def _member(line: str) -> str:
    src = f"@startuml\nclass C {{\n  {line}\n}}\n@enduml\n"
    out = format_text(src)
    assert format_text(out) == out, "idempotency"
    return out.splitlines()[2].strip()


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
    src = f"@startuml\nclass C {{\n  {line}\n}}\n@enduml\n"
    out = format_text(src)
    assert "".join(out.split()) == "".join(src.split())
    assert format_text(out) == out
