from typing import Annotated
import typer
import logging
from pathlib import Path

from actions.analyze import Analyzer
from actions.upload import Metadata, upload
from env import load_env

def main(
    filepath: Annotated[Path, typer.Argument(help='Path to the manga file or folder', exists=True)],
    verbose: bool = typer.Option(False, '--verbose', '-v', help='Verbose mode'),
    title: str = typer.Option(None, '--title', '-t', help='Title of the manga', prompt=True),
    author: str = typer.Option(None, '--author', '-a', help='Author of the manga', prompt=True),
    year: int = typer.Option(None, '--year', '-y', help='Year of the manga', prompt=True),
    volume: int = typer.Option(None, '--volume', '-v', help='Volume of the manga', prompt=True),
) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    metadata = Metadata(title, author, year, volume)

    analyzer = Analyzer()
    word_freq = analyzer.analyze(filepath)

    upload(metadata, word_freq)

if __name__ == '__main__':
    load_env()
    typer.run(main)
