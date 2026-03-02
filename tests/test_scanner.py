from pathlib import Path

from ctx.scanner import ScanResult, scan_project


def test_scan_detects_python(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'myapp'")
    result = scan_project(tmp_path)
    assert "Python" in result.stack


def test_scan_detects_node(tmp_path):
    (tmp_path / "package.json").write_text('{"name": "myapp"}')
    result = scan_project(tmp_path)
    assert "Node" in result.stack


def test_scan_captures_structure(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "main.py").write_text("")
    result = scan_project(tmp_path)
    assert "src" in result.structure


def test_scan_captures_readme(tmp_path):
    (tmp_path / "README.md").write_text("# MyApp\n\nA great app.")
    result = scan_project(tmp_path)
    assert "MyApp" in result.readme_summary


def test_scan_no_readme(tmp_path):
    result = scan_project(tmp_path)
    assert result.readme_summary == ""


def test_scan_empty_project(tmp_path):
    result = scan_project(tmp_path)
    assert isinstance(result.stack, list)
    assert isinstance(result.structure, str)
    assert isinstance(result.git_log, list)


def test_scan_result_to_markdown(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'myapp'")
    (tmp_path / "README.md").write_text("# MyApp\n\nA great app.")
    result = scan_project(tmp_path)
    md = result.to_markdown("myapp")
    assert "## Stack" in md
    assert "## Structure" in md
    assert "## Notes" in md
