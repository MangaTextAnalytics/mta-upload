import logging

from .env import env
from typing import Dict
from supabase.client import Client, create_client

logger = logging.getLogger(__name__)

class Manga:
    def __init__(self, title: str, author: str, year: int, volume: int):
        self.title = title
        self.author = author
        self.year = year
        self.volume = volume

def upload(manga: Manga, word_freq: Dict[str, int]):
    supabase: Client = create_client(env["SUPABASE_URL"], env["SUPABASE_KEY"])

    manga_id = upload_manga(supabase, manga)
    for word, count in word_freq.items():
        put_term(supabase, word)
        put_frequency(supabase, manga_id, word, count)
        

def upload_manga(supabase: Client, manga: Manga) -> int:
    """Upload the metadata of a manga to the database.

    Args:
        supabase (Client): The Supabase client.
        metadata (Metadata): The metadata of the manga.

    Returns:
        int: The ID of the manga.
    """

    resp = supabase.from_("Manga").insert({
        "title": manga.title,
        "author": manga.author,
        "year": manga.year,
        "volume": manga.volume
    }).execute()

    return resp.data[0]["id"]

def put_term(supabase: Client, term: str):
    """Puts the term in the table if it doesn't exist."""

    resp = supabase.from_("Term").select("*").eq("term", term).execute()
    if len(resp.data) == 0:
        resp = supabase.from_("Term").insert({"term": term}).execute()

def put_frequency(supabase: Client, manga_id: int, term: str, count: int):
    """Puts the frequency of a term in a manga in the database."""

    supabase.from_("Frequency").insert({
        "manga_id": manga_id,
        "termTerm": term,
        "count": count
    }).execute()
