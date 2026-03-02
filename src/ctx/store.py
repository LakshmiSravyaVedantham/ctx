from dataclasses import dataclass
from pathlib import Path

GLOBAL_DIR = Path.home() / ".ctx" / "packs"


@dataclass
class Pack:
    name: str
    content: str


class PackStore:
    def __init__(self, global_dir: Path = GLOBAL_DIR) -> None:
        self.global_dir = global_dir

    def save(self, pack: Pack, scope: str = "global", local_dir: Path | None = None) -> None:
        target = (local_dir or Path(".ctx")) if scope == "local" else self.global_dir
        target.mkdir(parents=True, exist_ok=True)
        (target / f"{pack.name}.md").write_text(pack.content)

    def load(self, name: str, local_dir: Path | None = None) -> Pack | None:
        local = (local_dir or Path(".ctx")) / f"{name}.md"
        if local.exists():
            return Pack(name=name, content=local.read_text())
        global_path = self.global_dir / f"{name}.md"
        if global_path.exists():
            return Pack(name=name, content=global_path.read_text())
        return None

    def delete(self, name: str, local_dir: Path | None = None) -> None:
        local = (local_dir or Path(".ctx")) / f"{name}.md"
        if local.exists():
            local.unlink()
        global_path = self.global_dir / f"{name}.md"
        if global_path.exists():
            global_path.unlink()

    def list_all(self, local_dir: Path | None = None) -> list[Pack]:
        seen: dict[str, Pack] = {}
        local = local_dir or Path(".ctx")
        if local.exists():
            for f in sorted(local.glob("*.md")):
                seen[f.stem] = Pack(name=f.stem, content=f.read_text())
        if self.global_dir.exists():
            for f in sorted(self.global_dir.glob("*.md")):
                if f.stem not in seen:
                    seen[f.stem] = Pack(name=f.stem, content=f.read_text())
        return list(seen.values())
