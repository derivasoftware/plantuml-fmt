"""CLI behaviour: check mode, write mode, idempotent second run."""

from plantuml_fmt.cli import main

MESSY = "@startuml\n   class Foo\n@enduml\n"


def test_check_then_write_then_clean(tmp_path, capsys):
    f = tmp_path / "d.puml"
    f.write_text(MESSY)

    assert main(["--check", str(tmp_path)]) == 1
    assert str(f) in capsys.readouterr().out
    assert f.read_text() == MESSY

    assert main([str(tmp_path)]) == 0
    assert f.read_text() == "@startuml\nclass Foo\n@enduml\n"

    assert main(["--check", str(tmp_path)]) == 0
