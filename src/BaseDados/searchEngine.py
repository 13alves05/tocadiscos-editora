# --- Add these imports at the top ---
import os
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.qparser import MultifieldParser

# --- Define Whoosh schema (only for search) ---
search_schema = Schema(
    track_id=ID(stored=True, unique=True),
    track_title=TEXT(stored=True),
    artist_name=TEXT(stored=True),
    album_title=TEXT(stored=True),
    track_genres=TEXT(stored=True),
    artist_nacionality=TEXT(stored=True),
    track_price=STORED,
    track_interest=STORED,
)

INDEX_DIR = "music_search_index"

def build_search_index_from_raw_lines(validated_lines):
    """Call this once after processing your CSV"""
    if os.path.exists(INDEX_DIR):
        import shutil
        shutil.rmtree(INDEX_DIR)
    os.mkdir(INDEX_DIR)
    
    ix = create_in(INDEX_DIR, search_schema)
    writer = ix.writer()
    
    for line in validated_lines:
        writer.add_document(
            track_id=line['track_id'],
            track_title=line['track_title'],
            artist_name=line['artist_name'],
            album_title=line['album_title'],
            track_genres=line['track_genres'],
            artist_nacionality=line['artist_nacionality'],
            track_price=line['track_price'],
            track_interest=line['track_interest'],
        )
    
    writer.commit()
    print(f"Search index built with {len(validated_lines)} tracks.")

def search_tracks(query_str, limit=20):
    """Call this whenever you want to search"""
    if not exists_in(INDEX_DIR):
        print("No search index found. Build it first.")
        return []
    
    ix = open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        parser = MultifieldParser(
            ["track_title", "artist_name", "album_title", "track_genres", "artist_nacionality"],
            ix.schema
        )
        query = parser.parse(query_str)
        results = searcher.search(query, limit=limit)
        
        return [hit.fields() for hit in results]  # returns list of dicts