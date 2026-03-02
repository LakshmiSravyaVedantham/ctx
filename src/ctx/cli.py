"""CLI entry point for ctx."""

from pathlib import Path

import click

from ctx import __version__
from ctx.injector import inject_claude, inject_clipboard
from ctx.scanner import scan_project
from ctx.store import Pack, PackStore

_store = PackStore()


def _local_dir() -> Path:
    return Path.cwd() / ".ctx"


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """ctx — Save project context packs. Inject into Claude, ChatGPT, or clipboard."""


@main.command()
@click.argument("name")
@click.option(
    "--notes", default="", help="Add notes directly (skips interactive prompt)"
)
@click.option(
    "--scope",
    default="global",
    type=click.Choice(["global", "local"]),
    help="Where to save the pack",
)
def save(name: str, notes: str, scope: str) -> None:
    """Scan current project and save as a context pack."""
    click.echo(f"Scanning {Path.cwd().name} ...")
    result = scan_project(Path.cwd())
    content = result.to_markdown(name)

    if notes:
        content = content.replace("(add your notes here)", notes)
    else:
        click.echo("Add notes (press Enter twice when done, leave blank to skip):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        user_notes = "\n".join(lines).strip()
        if user_notes:
            content = content.replace("(add your notes here)", user_notes)

    pack = Pack(name=name, content=content)
    _store.save(pack, scope=scope, local_dir=_local_dir())
    click.echo(f"Saved '{name}' ({scope}).")


@main.command(name="list")
def list_cmd() -> None:
    """List all saved context packs."""
    packs = _store.list_all(local_dir=_local_dir())
    if not packs:
        click.echo("No context packs saved yet. Run: ctx save <name>")
        return
    click.echo("Context packs:")
    for pack in packs:
        scope = "local" if (_local_dir() / f"{pack.name}.md").exists() else "global"
        click.echo(f"  {pack.name:20s} [{scope}]")


@main.command()
@click.argument("name")
def show(name: str) -> None:
    """Print a context pack."""
    pack = _store.load(name, local_dir=_local_dir())
    if not pack:
        click.echo(f"No pack named '{name}'. Run: ctx list", err=True)
        raise SystemExit(1)
    click.echo(pack.content)


@main.command()
@click.argument("name")
@click.option(
    "--target",
    default="clipboard",
    type=click.Choice(["claude", "clipboard", "chatgpt"]),
    help="Where to inject",
)
def inject(name: str, target: str) -> None:
    """Inject a context pack into Claude Code or clipboard."""
    pack = _store.load(name, local_dir=_local_dir())
    if not pack:
        click.echo(f"No pack named '{name}'. Run: ctx list", err=True)
        raise SystemExit(1)

    if target == "claude":
        result = inject_claude(pack.content)
    elif target == "chatgpt":
        result = inject_clipboard(f"System context:\n\n{pack.content}")
    else:
        result = inject_clipboard(pack.content)

    if result.success:
        click.echo(result.message)
    else:
        click.echo(f"Error: {result.message}", err=True)
        raise SystemExit(1)


@main.command()
@click.argument("name")
def delete(name: str) -> None:
    """Delete a context pack."""
    pack = _store.load(name, local_dir=_local_dir())
    if not pack:
        click.echo(f"No pack named '{name}'.", err=True)
        raise SystemExit(1)
    _store.delete(name, local_dir=_local_dir())
    click.echo(f"Deleted '{name}'.")


@main.command()
@click.argument("name")
def edit(name: str) -> None:
    """Open a context pack in $EDITOR."""
    pack = _store.load(name, local_dir=_local_dir())
    if not pack:
        click.echo(f"No pack named '{name}'.", err=True)
        raise SystemExit(1)
    local = _local_dir() / f"{name}.md"
    path = local if local.exists() else PackStore().global_dir / f"{name}.md"
    click.edit(filename=str(path))
