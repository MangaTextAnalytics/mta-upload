import logging
from manga_ocr import MangaOcr

# create a singleton instance of MangaOcr
mocr = MangaOcr()

# parse a filepath
def parse(filepath: str) -> str:
    logging.info('Parsing file=%s', filepath)
    return mocr(filepath)
