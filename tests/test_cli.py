from pathlib import Path
from click.testing import CliRunner
from ctx.cli import main


def test_help():
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "ctx" in result.output.lower()


def test_list_empty():
    result = CliRunner().invoke(main, ["list"], catch_exceptions=False)
    assert result.exit_code == 0


def test_save_and_show(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ["save", "myproject", "--notes", "Python API project", "--scope", "local"])
        assert result.exit_code == 0, result.output
        assert "saved" in result.output.lower()

        result = runner.invoke(main, ["show", "myproject"])
        assert result.exit_code == 0
        assert "myproject" in result.output


def test_inject_claude(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        runner.invoke(main, ["save", "myproject", "--notes", "Python project", "--scope", "local"])
        result = runner.invoke(main, ["inject", "myproject", "--target", "claude"])
        assert result.exit_code == 0, result.output
        assert Path("CLAUDE.md").exists()


def test_delete(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        runner.invoke(main, ["save", "myproject", "--notes", "test", "--scope", "local"])
        result = runner.invoke(main, ["delete", "myproject"])
        assert result.exit_code == 0
