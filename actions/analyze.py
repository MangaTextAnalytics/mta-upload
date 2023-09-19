import os
import logging

from typing import Dict
from manga_ocr import MangaOcr
from janome.tokenfilter import TokenCountFilter
from janome.analyzer import Analyzer as JanomeAnalyzer

class Analyzer:
    def __init__(self):
        self.mocr = MangaOcr()
        self.janome_analyzer = JanomeAnalyzer(token_filters=[TokenCountFilter()])

    def parse(self, filepath: str) -> str:
        logging.info('Parsing file=%s', filepath)
        return self.mocr(filepath)

    def count_freq(self, text: str) -> Dict[str, int]:
        freq = {}
        for k, v in self.janome_analyzer.analyze(text):
            freq[k] = v
        return freq

    def analyze(self, filepath: str) -> Dict[str, int]:
        freq = {}
        if os.path.isdir(filepath):
            if not filepath.endswith('/'):
                filepath += '/'
            for path in os.listdir(filepath):
                for k, v in self.analyze(filepath + path).items():
                    freq[k] = freq.get(k, 0) + v
        else: 
            text = self.parse(filepath)
            freq = self.count_freq(text)
        return freq

        

