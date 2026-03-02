import subprocess
from dataclasses import dataclass, field
from pathlib import Path

STACK_INDICATORS: list[tuple[str, str]] = [
    ("pyproject.toml", "Python"),
    ("requirements.txt", "Python"),
    ("setup.py", "Python"),
    ("package.json", "Node"),
    ("go.mod", "Go"),
    ("Cargo.toml", "Rust"),
    ("pom.xml", "Java"),
    ("Gemfile", "Ruby"),
]


@dataclass
class ScanResult:
    stack: list[str] = field(default_factory=list)
    structure: str = ""
    git_log: list[str] = field(default_factory=list)
    readme_summary: str = ""

    def to_markdown(self, name: str) -> str:
        lines = [f"# {name}", ""]
        if self.stack:
            lines += ["## Stack", "- " + "\n- ".join(self.stack), ""]
        if self.structure:
            lines += ["## Structure", "```", self.structure, "```", ""]
        if self.git_log:
            lines += ["## Recent commits"]
            lines += [f"- {e}" for e in self.git_log[:10]]
            lines += [""]
        if self.readme_summary:
            lines += ["## README", self.readme_summary, ""]
        lines += ["## Notes", "(add your notes here)", ""]
        return "\n".join(lines)


def _detect_stack(root: Path) -> list[str]:
    found = []
    for filename, label in STACK_INDICATORS:
        if (root / filename).exists() and label not in found:
            found.append(label)
    return found


def _build_structure(root: Path, depth: int = 2) -> str:
    lines: list[str] = []

    def walk(path: Path, prefix: str, current_depth: int) -> None:
        if current_depth > depth:
            return
        entries = sorted(
            [e for e in path.iterdir() if not e.name.startswith(".")],
            key=lambda e: (e.is_file(), e.name),
        )
        for entry in entries[:20]:
            lines.append(f"{prefix}{entry.name}{'/' if entry.is_dir() else ''}")
            if entry.is_dir() and current_depth < depth:
                walk(entry, prefix + "  ", current_depth + 1)

    walk(root, "", 1)
    return "\n".join(lines)


def _get_git_log(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            capture_output=True,
            text=True,
            cwd=root,
            timeout=5,
        )
        if result.returncode == 0:
            return [
                line.split(" ", 1)[1]
                for line in result.stdout.strip().splitlines()
                if " " in line
            ]
    except Exception:
        pass
    return []


def _get_readme_summary(root: Path, max_chars: int = 300) -> str:
    readme = root / "README.md"
    if not readme.exists():
        return ""
    text = readme.read_text(errors="ignore")
    lines = [line for line in text.splitlines() if line.strip()]
    return " ".join(lines)[:max_chars]


def scan_project(root: Path) -> ScanResult:
    return ScanResult(
        stack=_detect_stack(root),
        structure=_build_structure(root),
        git_log=_get_git_log(root),
        readme_summary=_get_readme_summary(root),
    )
