import csv
import os
import shutil
from pathlib import Path

from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD
from whoosh.qparser import MultifieldParser

# Esquema unificado
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
    """Constrói o índice de busca unificado Whoosh a partir dos três ficheiros CSV"""
    print("Inicializando o programa.")
    
    # Limpa e recria o diretório do índice
    if os.path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)
    os.makedirs(INDEX_DIR, exist_ok=True)

    ix = create_in(INDEX_DIR, unified_schema)
    writer = ix.writer()

    total_docs = 0

    # =========================== Músicas ===========================
    tracks_path = Path(tracks_file)
    if tracks_path.exists():
        try:
            with open(tracks_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    print(f"Erro: Sem cabeçalho em {tracks_file}")
                else:
                    reader.fieldnames = [name.strip() for name in reader.fieldnames]
                    for row in reader:
                        try:
                            nationality = row.get('artist_nacionality', '') or row.get('artist_nacionality ', '')
                            price = row.get('track_price', '') or row.get('track_price ', '')

                            writer.add_document(
                                doc_type="track",
                                doc_id=f"track_{row['track_id']}",
                                title=row.get('track_title', ''),
                                artist_name=row.get('artist_name', ''),
                                genres=row.get('track_genres', ''),
                                nationality=nationality,

                                album_title=row.get('album_title', ''),
                                track_title=row.get('track_title', ''),
                                track_price=price,
                            )
                            total_docs += 1
                        except Exception as e:
                            print(f"Erro ao indexar track {row.get('track_id')}: {e}")
                            continue
        except Exception as e:
            print(f"Erro ao abrir {tracks_file}: {e}")
    else:
        print(f"Aviso: Ficheiro de tracks não encontrado: {tracks_file}")

    # =========================== Álbuns ===========================
    albums_path = Path(albums_file)
    if albums_path.exists():
        try:
            with open(albums_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    print(f"Erro: Sem cabeçalho em {albums_file}")
                else:
                    reader.fieldnames = [name.strip() for name in reader.fieldnames]
                    for row in reader:
                        try:
                            writer.add_document(
                                doc_type="album",
                                doc_id=f"album_{row['album_id']}",
                                title=row.get('album_title', ''),
                                artist_name=row.get('artist_name', ''),
                                genres=row.get('album_genere', ''),
                                nationality='',

                                album_title=row.get('album_title', ''),
                                unites_sold=row.get('unites_sold', ''),
                                album_price=row.get('album_price', ''),
                                album_date=row.get('album_date', ''),
                                track_list=row.get('tracks', ''),
                            )
                            total_docs += 1
                        except Exception as e:
                            print(f"Erro ao indexar álbum {row.get('album_id')}: {e}")
                            continue
        except Exception as e:
            print(f"Erro ao abrir {albums_file}: {e}")
    else:
        print(f"Aviso: Ficheiro de álbuns não encontrado: {albums_file}")

    # =========================== Autores ===========================
    authors_path = Path(authors_file)
    if authors_path.exists():
        try:
            with open(authors_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    print(f"Erro: Sem cabeçalho em {authors_file}")
                else:
                    reader.fieldnames = [name.strip() for name in reader.fieldnames]
                    for row in reader:
                        try:
                            writer.add_document(
                                doc_type="artist",
                                doc_id=f"artist_{row['author_id']}",
                                title=row.get('artist_name', ''),
                                artist_name=row.get('artist_name', ''),
                                genres='',
                                nationality=row.get('artist_nacionality', ''),

                                total_earned=row.get('total_earned', ''),
                                rights_percentage=row.get('rights_percentage', ''),
                                album_list=row.get('album_title', ''),
                            )
                            total_docs += 1
                        except Exception as e:
                            print(f"Erro ao indexar autor {row.get('author_id')}: {e}")
                            continue
        except Exception as e:
            print(f"Erro ao abrir {authors_file}: {e}")
    else:
        print(f"Aviso: Ficheiro de autores não encontrado: {authors_file}")

    # Finaliza o índice
    writer.commit()
    print(f"\nÍndice construído com sucesso: {total_docs} documentos indexados.")
    print("Programa inicializado com sucesso\n")


def search(query_str, limit=20, filter_type=None):
    """Pesquisa em tracks, álbuns e autores"""
    if not exists_in(INDEX_DIR):
        print("Índice não encontrado. Execute build_unified_index() primeiro.")
        return []

    ix = open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "artist_name", "genres", "nationality"], ix.schema)
        query = parser.parse(query_str)
        results = searcher.search(query, limit=limit)

        if filter_type:
            results = [hit for hit in results if hit['doc_type'] == filter_type]

        return [hit.fields() for hit in results]