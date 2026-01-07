import csv
import os
import shutil
from pathlib import Path

from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, STORED, KEYWORD
from whoosh.qparser import MultifieldParser

# Este módulo é responsável por criar e gerir um índice de pesquisa unificado
# usando a biblioteca Whoosh. O objetivo é acelerar pesquisas por texto
# (autor, álbum, música) sem ter de percorrer os CSV manualmente.

# O schema define a estrutura dos documentos que vão ser indexados.
# Cada documento pode ser de 3 tipos: track, album ou artist.
unified_schema = Schema(
    doc_type=KEYWORD(stored=True),   # tipo do documento (track/album/artist)
    doc_id=ID(stored=True, unique=True),  # identificador único no índice

    # Campos pesquisáveis
    title=TEXT(stored=True),
    artist_name=TEXT(stored=True),
    genres=TEXT(stored=True),
    nationality=TEXT(stored=True),

    # Campos adicionais guardados apenas para consulta (não pesquisáveis)
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

# Diretório onde o índice Whoosh será guardado
INDEX_DIR = "unified_music_index"


def build_unified_index(
    tracks_file="data/raw_tracks.csv",
    albums_file="data/albums_table.csv",
    authors_file="data/authors_table.csv"
):
    """
    Constrói o índice de pesquisa unificado a partir dos três CSV principais.
    Este processo:
      - apaga o índice antigo
      - cria um novo
      - percorre músicas, álbuns e autores
      - adiciona cada entrada como documento Whoosh
    """

    print("Inicializando o programa.")
    
    # Se já existir um índice, apagamos tudo para garantir consistência
    if os.path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)
    os.makedirs(INDEX_DIR, exist_ok=True)

    # Criação do índice com o schema definido acima
    ix = create_in(INDEX_DIR, unified_schema)
    writer = ix.writer()

    total_docs = 0  # contador de documentos indexados

    # =========================== Músicas ===========================
    # Cada linha do CSV de músicas é indexada como documento do tipo "track".
    tracks_path = Path(tracks_file)
    if tracks_path.exists():
        try:
            with open(tracks_path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)

                # Verificação básica de integridade do CSV
                if reader.fieldnames is None:
                    print(f"Erro: Sem cabeçalho em {tracks_file}")
                else:
                    # Remove espaços nos nomes das colunas
                    reader.fieldnames = [name.strip() for name in reader.fieldnames]

                    for row in reader:
                        try:
                            # Alguns CSV podem ter espaços extra nos nomes das colunas
                            nationality = (row.get('artist_nacionality') or row.get('artist_nacionality ') or '')
                            price = (row.get('track_price') or row.get('track_price ') or '')

                            # Adiciona documento ao índice
                            writer.add_document(
                                doc_type="track",
                                doc_id=f"track_{row.get('track_id', '')}",
                                title=(row.get('track_title') or ''),
                                artist_name=(row.get('artist_name') or ''),
                                genres=(row.get('track_genres') or ''),
                                nationality=nationality,

                                album_title=(row.get('album_title') or ''),
                                track_title=(row.get('track_title') or ''),
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
    # Cada álbum é indexado como documento do tipo "album".
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
                                doc_id=f"album_{row.get('album_id', '')}",
                                title=(row.get('album_title') or ''),
                                artist_name=(row.get('artist_name') or ''),
                                genres=(row.get('album_genere') or ''),
                                nationality='',  # álbuns não têm nacionalidade

                                album_title=(row.get('album_title') or ''),
                                unites_sold=(row.get('unites_sold') or ''),
                                album_price=(row.get('album_price') or ''),
                                album_date=(row.get('album_date') or ''),
                                track_list=(row.get('tracks') or ''),
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
    # Cada autor é indexado como documento do tipo "artist".
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
                                doc_id=f"artist_{row.get('author_id', '')}",
                                title=(row.get('artist_name') or ''),
                                artist_name=(row.get('artist_name') or ''),
                                genres='',
                                nationality=(row.get('artist_nacionality') or ''),

                                total_earned=(row.get('total_earned') or ''),
                                rights_percentage=(row.get('rights_percentage') or ''),
                                album_list=(row.get('album_title') or ''),
                            )

                            total_docs += 1

                        except Exception as e:
                            print(f"Erro ao indexar autor {row.get('author_id')}: {e}")
                            continue

        except Exception as e:
            print(f"Erro ao abrir {authors_file}: {e}")

    else:
        print(f"Aviso: Ficheiro de autores não encontrado: {authors_file}")

    # Finaliza o índice e grava tudo no disco
    writer.commit()
    print("Programa inicializado com sucesso\n")


def search(query_str, limit=20, filter_type=None):
    """
    Pesquisa no índice unificado.
    Pode procurar por:
      - tracks
      - álbuns
      - autores

    O parâmetro filter_type permite filtrar resultados por tipo.
    """

    if not exists_in(INDEX_DIR):
        print("Índice não encontrado. Execute build_unified_index() primeiro.")
        return []

    ix = open_dir(INDEX_DIR)

    with ix.searcher() as searcher:
        # Parser que permite pesquisar em vários campos ao mesmo tempo
        parser = MultifieldParser(["title", "artist_name", "genres", "nationality"], ix.schema)
        query = parser.parse(query_str)

        # Executa a pesquisa
        results = searcher.search(query, limit=limit)

        # Se o utilizador quiser filtrar por tipo (track/album/artist)
        if filter_type:
            results = [hit for hit in results if hit['doc_type'] == filter_type]

        # Converte os resultados para dicionários simples
        return [hit.fields() for hit in results]