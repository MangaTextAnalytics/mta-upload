from typing import Dict

class Metadata:
    def __init__(self, title: str, author: str, year: int, volume: int):
        self.title = title
        self.author = author
        self.year = year
        self.volume = volume

def upload(metadata: Metadata, word_freq: Dict[str, int]):
    print('Uploading metadata=%s, word_freq=%s' % (metadata, word_freq))
