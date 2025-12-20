import csv
import os
import shutil
from pathlib import Path

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD
from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import MultifieldParser

# Unified schema (unchanged)
unified_schema = Schema(
    doc_type=KEYWORD(stored=True),
    doc_id=ID(stored=True, unique=True),

    title=TEXT(stored=True),
    artist_name=TEXT(stored=True),
    genres=TEXT(stored=True),
    nationality=TEXT(stored=True),

    album_title=STORED(),
    track_title=STORED(),
    total_earned=STORED(),
    unites_sold=STORED(),
    album_price=STORED(),
    track_price=STORED(),
    rights_percentage=STORED(),
    album_date=STORED(),
    track_list=STORED(),
    album_list=STORED(),
)

INDEX_DIR = "unified_music_index"

def build_unified_index(
    tracks_file="data/raw_tracks.csv",
    albums_file="data/albums_table.csv",
    authors_file="data/authors_table.csv"
):
    """Build the unified Whoosh search index from your three CSV files"""
    
    # Clean and recreate index directory
    if os.path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)
    os.mkdir(INDEX_DIR)

    ix = create_in(INDEX_DIR, unified_schema)
    writer = ix.writer()

    total_docs = 0

    # =========================== TRACKS ===========================
    if Path(tracks_file).exists():
        with open(tracks_file, newline='', encoding='utf-8') as f:  # Changed back to utf-8
            reader = csv.DictReader(f)
            # Strip BOM and whitespace from fieldnames manually
            reader.fieldnames = [name.lstrip('\ufeff').strip() for name in reader.fieldnames]
            print(f"Indexing tracks — columns: {reader.fieldnames}")

            for row in reader:
                # Duplicate columns: use the first one (they are identical)
                nationality = row['artist_nacionality']
                price = row['track_price']

                writer.add_document(
                    doc_type="track",
                    doc_id=f"track_{row['track_id']}",
                    title=row['track_title'],
                    artist_name=row['artist_name'],
                    genres=row['track_genres'],
                    nationality=nationality,
                    album_title=row['album_title'],
                    track_title=row['track_title'],
                    track_price=price,
                )
                total_docs += 1
    else:
        print(f"Warning: Tracks file not found: {tracks_file}")

    # =========================== ALBUMS ===========================
    if Path(albums_file).exists():
        with open(albums_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.lstrip('\ufeff').strip() for name in reader.fieldnames]
            print(f"Indexing albums — columns: {reader.fieldnames}")

            for row in reader:
                track_list = row.get('tracks', '')

                writer.add_document(
                    doc_type="album",
                    doc_id=f"album_{row['album_id']}",
                    title=row['album_title'],
                    artist_name=row['artist_name'],
                    genres=row.get('album_genere', ''),
                    nationality="",
                    album_title=row['album_title'],
                    unites_sold=row.get('unites_sold', ''),
                    album_price=row.get('album_price', ''),
                    album_date=row.get('album_date', ''),
                    track_list=track_list,
                )
                total_docs += 1
    else:
        print(f"Warning: Albums file not found: {albums_file}")

    # =========================== ARTISTS ===========================
    if Path(authors_file).exists():
        with open(authors_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.lstrip('\ufeff').strip() for name in reader.fieldnames]
            print(f"Indexing artists — columns: {reader.fieldnames}")

            for row in reader:
                album_list = row.get('album_title', '')

                writer.add_document(
                    doc_type="artist",
                    doc_id=f"artist_{row['author_id']}",  # Note: author_id in your file
                    title=row['artist_name'],
                    artist_name=row['artist_name'],
                    genres="",
                    nationality=row['artist_nacionality'],
                    total_earned=row.get('total_earned', ''),
                    rights_percentage=row.get('rights_percentage', ''),
                    album_list=album_list,
                )
                total_docs += 1
    else:
        print(f"Warning: Artists file not found: {authors_file}")

    # Finalize index
    writer.commit()
    print(f"\nUnified search index built successfully with {total_docs} items (tracks + albums + artists)!")

def search(query_str, limit=20, filter_type=None):
    """Search across tracks, albums, and artists"""
    if not exists_in(INDEX_DIR):
        print("Index not found. Run build_unified_index() first.")
        return []

    ix = open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "artist_name", "genres", "nationality"], ix.schema)
        query = parser.parse(query_str)
        results = searcher.search(query, limit=limit)

        if filter_type:
            results = [r for r in results if r['doc_type'] == filter_type]

        hits = [r.fields() for r in results]
        
        # Optional: sort by relevance score descending
        # hits.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return hits

# =============================================================================
# === TEST / RUN DIRECTLY BELOW ===============================================
# =============================================================================

# 1. Build the index (run this once or whenever your CSVs change)
build_unified_index()

# 2. Try some searches
teste = input('pesquisa:  ')
for q in [teste]:
    print(f"\nSearch: '{q}'")
    results = search(q, limit=10)
    for r in results:
        if r['doc_type'] == 'track':
            print(f"   🎵 {r['track_title']} by {r['artist_name']} ({r['album_title']})")
        elif r['doc_type'] == 'album':
            print(f"   💿 Album: {r['title']} by {r['artist_name']} — Sold: {r.get('unites_sold', 'N/A')}")
        elif r['doc_type'] == 'artist':
            print(f"   👤 Artist: {r['title']} ({r['nationality']}) — Earned: ${r.get('total_earned', 'N/A')}")
    print(f"   --- {len(results)} results ---")