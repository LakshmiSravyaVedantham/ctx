from dataclasses import dataclass
from pathlib import Path


@dataclass
class InjectionResult:
    success: bool
    message: str
    target: str = ""


def inject_claude(content: str, target_dir: Path | None = None) -> InjectionResult:
    """Write content to CLAUDE.md in target_dir."""
    target = (target_dir or Path.cwd()) / "CLAUDE.md"
    try:
        target.write_text(content)
        return InjectionResult(success=True, message=f"Written to {target}", target=str(target))
    except Exception as e:
        return InjectionResult(success=False, message=str(e))


def inject_clipboard(content: str) -> InjectionResult:
    """Copy content to clipboard."""
    try:
        import pyperclip
        pyperclip.copy(content)
        return InjectionResult(success=True, message="Copied to clipboard — paste into any AI chat.")
    except Exception as e:
        return InjectionResult(success=False, message=f"Could not copy to clipboard: {e}")
