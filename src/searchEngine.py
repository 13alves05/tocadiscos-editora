import csv
import os
import shutil
from pathlib import Path

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD
from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import MultifieldParser

# Esquema unificado (inalterado)
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
    os.mkdir(INDEX_DIR)

    ix = create_in(INDEX_DIR, unified_schema)
    writer = ix.writer()

    total_docs = 0

    # =========================== Músicas ===========================
    if Path(tracks_file).exists():
        with open(tracks_file, newline='', encoding='utf-8') as f:  # Alterado para utf-8
            reader = csv.DictReader(f)
            # Remove BOM e espaços dos nomes dos campos manualmente
            reader.fieldnames = [name.lstrip('\ufeff').strip() for name in reader.fieldnames]
            # print(f"Indexando tracks — colunas: {reader.fieldnames}")

            for row in reader:
                # Colunas duplicadas: usa a primeira (são idênticas)
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
        print(f"Aviso: Ficheiro de tracks não encontrado: {tracks_file}")

    # =========================== Albuns ===========================
    if Path(albums_file).exists():
        with open(albums_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.lstrip('\ufeff').strip() for name in reader.fieldnames]
            # print(f"Indexando álbuns — colunas: {reader.fieldnames}")

            for row in reader:
                writer.add_document(
                    doc_type="album",
                    doc_id=f"album_{row['album_id']}",
                    title=row['album_title'],
                    artist_name=row['artist_name'],
                    genres=row['album_genere'],
                    nationality=row.get('artist_nacionality', ''),

                    album_title=row['album_title'],
                    unites_sold=row['unites_sold'],
                    album_price=row['album_price'],
                    album_date=row['album_date'],
                    track_list=row['tracks'],
                )
                total_docs += 1
    else:
        print(f"Aviso: Ficheiro de álbuns não encontrado: {albums_file}")

    # =========================== Autores ===========================
    if Path(authors_file).exists():
        with open(authors_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.lstrip('\ufeff').strip() for name in reader.fieldnames]
            # print(f"Indexando autores — colunas: {reader.fieldnames}")

            for row in reader:
                # Lista de álbuns como string para armazenar
                album_list = row['album_title']

                writer.add_document(
                    doc_type="artist",
                    doc_id=f"artist_{row['author_id']}",
                    title=row['artist_name'],
                    artist_name=row['artist_name'],
                    genres='',  # Autores não têm géneros diretos
                    nationality=row['artist_nacionality'],

                    total_earned=row['total_earned'],
                    rights_percentage=row.get('rights_percentage', ''),
                    album_list=album_list,
                )
                total_docs += 1
    else:
        print(f"Aviso: Ficheiro de autores não encontrado: {authors_file}")

    # Finaliza o índice
    writer.commit()
    # print(f"\nÍndice de busca unificado construído com sucesso com {total_docs} itens (tracks + álbuns + autores)!")
    print("\nPrograma inicializado com sucesso\n")

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
            results = [r for r in results if r['doc_type'] == filter_type]

        hits = [r.fields() for r in results]
        
        # Opcional: ordena por pontuação de relevância descendente
        # hits.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return hits

# build_unified_index()

# import ast    

# resultados = search('awol', limit=20, filter_type='album')
# album_tracks = resultados[0]['track_list']
# track_list = ast.literal_eval(album_tracks)

# print(track_list)