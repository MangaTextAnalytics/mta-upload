import logging

from .env import load_env, env
from typing import Any, Dict, List
from supabase.client import Client, create_client

logger = logging.getLogger(__name__)

load_env()
supabase: Client = create_client(env["SUPABASE_URL"], env["SUPABASE_KEY"])

class Manga:
    def __init__(self, title: str, author: str, year: int, volume: int):
        self.title = title
        self.author = author
        self.year = year
        self.volume = volume

def upload(manga_metadata: Manga, term_freq: Dict[str, int]):
    manga = get_manga_with_fallback(manga_metadata.title, manga_metadata)
    volume = put_volume(manga['id'], manga_metadata.volume)

    manga_freqs = []
    volume_freqs = []
    for term, count in term_freq.items():
        upsert_term(term, count)
        manga_freqs.append(calc_freq(manga['id'], True, term, count))
        volume_freqs.append(calc_freq(volume['id'], False, term, count))
    
    supabase.from_('Frequency').upsert(manga_freqs, on_conflict="termTerm, mangaId").execute()
    supabase.from_('Frequency').insert(volume_freqs).execute()

    manga_freqs = supabase.from_('Frequency').select('count').eq('mangaId', manga['id']).execute().data
    update_stats(manga['statsId'], manga_freqs)
    volume_freqs = supabase.from_('Frequency').select('count').eq('volumeId', volume['id']).execute().data
    update_stats(volume['statsId'], volume_freqs)


def get_manga_with_fallback(title: str, manga_metadata: Manga) -> Dict[str, Any]:
    """Get the manga from the database, or create it if it doesn't exist.
    
    Args:
        title (str): The title of the manga.
        manga_metadata (Manga): The metadata of the manga.

    Returns:
        Dict[str, Any]: The manga.
    """

    try:
        resp = supabase.from_('Manga').select('*').eq('title', title).execute()
        if len(resp.data) == 0 or resp.data[0] is None:
            raise Exception('manga not found. need to create it.')
        return resp.data[0]
    except Exception:
        # put dummy stats for now
        stats_resp = supabase.from_('Stats').insert({}).execute()
        # put manga
        resp = supabase.from_('Manga').insert({
            'title': manga_metadata.title,
            'author': manga_metadata.author,
            'year': manga_metadata.year,
            'statsId': stats_resp.data[0]['id'],
        }).execute()
        return resp.data[0]

def put_volume(manga_id: int, volume: int) -> Dict[str, Any]:
    """Put the volume in the database.

    Args:
        manga_id (int): The id of the manga.
        volume (int): The volume number.

    Returns:
        Dict[str, Any]: The volume.
    """

    # put dummy stats for now
    stats_resp = supabase.from_('Stats').insert({}).execute()
    try:
        # put volume
        resp = supabase.from_('Volume').insert({
            'mangaId': manga_id,
            'volume': volume,
            'statsId': stats_resp.data[0]['id'],
        }).execute()
        return resp.data[0]
    except Exception:
        supabase.from_('Stats').delete().eq('id', stats_resp.data[0]['id']).execute()
        print('volume already exists. exiting..')
        exit(1)

def upsert_term(term: str, count: int):
    """Upsert the terms in the database.

    Args:
        term_freq (Dict[str, int]): The terms and their frequencies.
    """

    try:
        curr = supabase.from_('Term').select('*').eq('term', term).execute().data[0]['totalCount']
    except Exception:
        curr = 0
    supabase.from_('Term').upsert({
        'term': term,
        'totalCount': curr + count,
    }).execute()

def calc_freq(owner_id: int, is_manga: bool, term: str, count: int) -> Dict[str, Any]:
    """Calculate the frequency based on the owner's current frequency.
    
    Args:
        owner_id (int): The id of the owner (manga or volume).
        is_manga (bool): Whether the owner is a manga (True) or volume (False).
        term (str): The term.
        count (int): The count of the term.

    Returns:
        Dict[str, Any]: The frequency.
    """

    key = 'mangaId' if is_manga else 'volumeId'
    try:
        curr = supabase.from_('Frequency').select('*').eq('termTerm', term).eq(key, owner_id).execute().data[0]['count']
    except Exception:
        curr = 0

    return {
        'termTerm': term,
        'count': curr + count,
        key: owner_id,
    }

def update_stats(stats_id: int, freqs: List[Dict[str, Any]]):
    """Update the stats in the database.

    Args:
        stats_id (int): The id of the stats.
        freqs (List[Freq]): The frequencies.
    """

    uniqueWords = 0
    totalWords = 0
    wordsUsedOnce = 0

    for freq in freqs:
        totalWords += freq['count']
        uniqueWords += 1
        if freq['count'] == 1:
            wordsUsedOnce += 1

    wordsUsedOncePct = 100 * wordsUsedOnce / uniqueWords

    supabase.from_('Stats').update({
        'uniqueWords': uniqueWords,
        'totalWords': totalWords,
        'wordsUsedOnce': wordsUsedOnce,
        'wordsUsedOncePct': wordsUsedOncePct,
    }).eq('id', stats_id).execute()
