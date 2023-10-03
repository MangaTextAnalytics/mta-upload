import logging

from typing import Dict
from pathlib import Path
from manga_ocr import MangaOcr
from janome.tokenfilter import TokenCountFilter
from janome.analyzer import Analyzer as JanomeAnalyzer

logger = logging.getLogger(__name__)

class Analyzer:
    def __init__(self):
        self.mocr = MangaOcr()
        self.janome_analyzer = JanomeAnalyzer(token_filters=[TokenCountFilter()])

    def parse(self, filepath: Path) -> str:
        logger.info('Parsing file=%s', filepath)
        return self.mocr(filepath)

    def count_freq(self, text: str) -> Dict[str, int]:
        freq = {}
        for k, v in self.janome_analyzer.analyze(text):
            freq[k] = v
        return freq

    def analyze(self, filepath: Path) -> Dict[str, int]:
        freq = {}
        if filepath.is_dir():
            for path in filepath.iterdir():
                for k, v in self.analyze(path).items():
                    freq[k] = freq.get(k, 0) + v
        else: 
            text = self.parse(filepath)
            freq = self.count_freq(text)
        return freq
