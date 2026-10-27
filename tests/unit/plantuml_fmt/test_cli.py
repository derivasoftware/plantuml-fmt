"""The command line: check mode lists, write mode rewrites."""

from pathlib import Path

from plantuml_fmt.cli import iter_files, main

__covers__ = (iter_files, main)

DIRTY = "@startuml\nA   -->   B\n@enduml\n"


class TestIterFiles:
    def test_walks_directories_for_plantuml_suffixes_only(self, tmp_path: Path) -> None:
        (tmp_path / "a.puml").write_text(DIRTY)
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "b.iuml").write_text(DIRTY)
        (tmp_path / "c.txt").write_text("x")
        assert [p.name for p in iter_files([str(tmp_path)])] == ["a.puml", "b.iuml"]


class TestMain:
    def test_check_lists_and_writes_nothing_then_write_fixes(
        self, tmp_path: Path, capsys
    ) -> None:
        f = tmp_path / "a.puml"
        f.write_text(DIRTY)
        assert main(["--check", str(f)]) == 1
        assert str(f) in capsys.readouterr().out and f.read_text() == DIRTY
        assert main([str(f)]) == 0
        assert f.read_text() == "@startuml\nA --> B\n@enduml\n"
        assert main(["--check", str(f)]) == 0
