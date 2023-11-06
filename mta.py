import typer
import logging

from pathlib import Path
from typing import Annotated
from actions.analyze import Analyzer
from actions.upload import Manga, upload

logger = logging.getLogger(__name__)

def main(
    filepath: Annotated[Path, typer.Argument(help='Path to the manga file or folder', exists=True)],
    verbose: bool = typer.Option(False, '--verbose', '-v', help='Verbose mode'),
    title: str = typer.Option(None, '--title', '-t', help='Title of the manga', prompt=True),
    author: str = typer.Option(None, '--author', '-a', help='Author of the manga', prompt=True),
    year: int = typer.Option(None, '--year', '-y', help='Year of the manga', prompt=True),
    volume: int = typer.Option(None, '--volume', '-v', help='Volume of the manga', prompt=True),
) -> None:
    logger.level = logging.DEBUG if verbose else logging.INFO
    logger.debug("verbose=%s", verbose)

    metadata = Manga(title, author, year, volume)

    analyzer = Analyzer()
    word_freq = analyzer.analyze(filepath)

    # print word_freq and metadata before prompting for confirmation
    typer.echo(f'{filepath} results...')
    for k, v in word_freq.items():
        typer.echo(f'{k}: {v}')

    typer.echo(f'title={metadata.title} author={metadata.author} year={metadata.year} volume={metadata.volume}')

    # prompt for confirmation
    if not typer.confirm('Upload to database?'):
        raise typer.Abort()


    typer.echo('Uploading to database...')
    upload(metadata, word_freq)

if __name__ == '__main__':
    typer.run(main)
