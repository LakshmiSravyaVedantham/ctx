"""CLI entry point for ctx."""

import click

from ctx import __version__


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """ctx — Save project context packs. Inject into Claude, ChatGPT, or clipboard."""
