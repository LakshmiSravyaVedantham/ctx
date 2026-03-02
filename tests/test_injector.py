from pathlib import Path
from unittest.mock import patch

from ctx.injector import InjectionResult, inject_claude, inject_clipboard


def test_inject_claude_writes_file(tmp_path):
    result = inject_claude("# myproject\n\nPython API.", target_dir=tmp_path)
    assert (tmp_path / "CLAUDE.md").exists()
    assert result.success is True
    assert result.target == str(tmp_path / "CLAUDE.md")


def test_inject_claude_overwrites(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("old content")
    inject_claude("new content", target_dir=tmp_path)
    assert (tmp_path / "CLAUDE.md").read_text() == "new content"


def test_inject_clipboard_calls_pyperclip():
    with patch("pyperclip.copy") as mock_copy:
        result = inject_clipboard("# myproject")
    mock_copy.assert_called_once_with("# myproject")
    assert result.success is True


def test_inject_clipboard_fallback_on_error():
    with patch("pyperclip.copy", side_effect=Exception("no clipboard")):
        result = inject_clipboard("# myproject")
    assert result.success is False
    assert "clipboard" in result.message.lower()


def test_inject_claude_result_has_message(tmp_path):
    result = inject_claude("content", target_dir=tmp_path)
    assert len(result.message) > 0
