"""
Operações de I/O para os ficheiros CSV autores, álbuns e músicas.
Implementa carregamento, escrita e operações CRUD com snapshots.
Validação dos dados é feita por `BaseDados.dataSchema`.
"""

import csv
import ast
from pathlib import Path
import pandas as pd
from history import salvar_snapshot
from BaseDados import dataSchema as dS  # Usamos os schemas de validação
from searchEngine import build_unified_index

# Este módulo é responsável por toda a leitura e escrita dos CSV.
# Também faz operações CRUD e cria snapshots antes de qualquer alteração.


# Caminhos dos ficheiros CSV usados pela aplicação
AUTHORS_FILE = Path("data/authors_table.csv")
ALBUMS_FILE = Path("data/albums_table.csv")
TRACKS_FILE = Path("data/raw_tracks.csv")

# Headers usados ao gravar os ficheiros — garantem consistência na escrita
AUTHORS_HEADER = [
    'author_id',
    'artist_name',
    'artist_nacionality',
    'album_title',
    'rights_percentage',
    'total_earned',
]

ALBUMS_HEADER = [
    'album_id',
    'album_title',
    'artist_name',
    'album_genere',
    'album_date',
    'unites_sold',
    'album_price',
    'tracks',
]

TRACKS_HEADER = [
    'track_id',
    'album_id',
    'album_title',
    'artist_id',
    'artist_name',
    'track_date_recorded',
    'track_genres',
    'track_interest',
    'track_number',
    'track_title',
    'artist_nacionality',
    'track_price',
]

# Estruturas em memória onde guardamos os dados carregados
autores = {}
albuns = {}

# ====================== CARREGAMENTO SEGURO ======================

def load_autores():
    """
    Carrega os autores do CSV para um dicionário.
    Converte o campo 'album_title' de string para lista.
    Linhas inválidas são ignoradas para evitar crashes.
    """

    if not AUTHORS_FILE.exists():
        return autores

    with open(AUTHORS_FILE, "r", encoding="utf-8-sig") as authors_file:
        authors_list = csv.DictReader(authors_file)

        for author in authors_list:
            try:
                # ID do autor tem de ser inteiro
                author_id = int(author['author_id'])

                # album_title vem como string, tentamos convertê-lo para lista
                album_str = author.get('album_title', [])
                try:
                    albums_list = ast.literal_eval(album_str)
                    if not isinstance(albums_list, list):
                        albums_list = []
                except (ValueError, SyntaxError):
                    # Se a string estiver mal formatada, tratamos como lista vazia
                    albums_list = []

                author['album_title'] = albums_list

                # Construímos o dicionário final do autor
                data = {
                    'artist_name': author['artist_name'].strip(),
                    'artist_nacionality': author['artist_nacionality'].strip(),
                    'album_title': albums_list,
                    'rights_percentage': float(author.get('rights_percentage', 0)),
                    'total_earned': float(author.get('total_earned', 0.0))
                }

                autores[author_id] = data

            except (ValueError, KeyError, TypeError):
                # Se houver erro na linha, simplesmente ignoramos
                continue

    return autores


def load_albuns():
    """
    Carrega os álbuns do CSV.
    Converte o campo 'tracks' de string para lista.
    Linhas inválidas são ignoradas.
    """

    if not ALBUMS_FILE.exists():
        return albuns

    with open(ALBUMS_FILE, "r", encoding="utf-8-sig") as albums_file:
        albums_list = csv.DictReader(albums_file)

        for album in albums_list:
            try:
                album_id = int(album['album_id'])

                # Conversão do campo tracks
                try:
                    tracks_list = ast.literal_eval(album['tracks'])
                    if not isinstance(tracks_list, list):
                        tracks_list = []
                except (ValueError, SyntaxError):
                    tracks_list = []

                album['tracks'] = tracks_list

                # Construção do dicionário final
                data = {
                    'album_title': (album.get('album_title') or '').strip(),
                    'artist_name': (album.get('artist_name') or '').strip(),
                    'album_genere': (album.get('album_genere') or '').strip(),
                    'album_date': (album.get('album_date') or '').strip(),
                    'unites_sold': int(album.get('unites_sold') or 0),
                    'album_price': float(album.get('album_price') or 0.0),
                    'tracks': tracks_list
                }

                albuns[album_id] = data

            except (ValueError, KeyError, TypeError):
                continue

    return albuns


def load_musicas():
    """
    Carrega as músicas usando pandas.
    Retorna uma lista de dicionários.
    """
    if not TRACKS_FILE.exists():
        return []

    df = pd.read_csv(TRACKS_FILE, encoding="utf-8-sig", keep_default_na=False)
    return df.to_dict(orient="records")


# ====================== GRAVAÇÃO SEGURA ======================

def save_autores(autores):
    """Grava os autores no CSV, sobrescrevendo o ficheiro."""
    if not autores:
        print("Não existem autores para Salvar")
        return

    with open(AUTHORS_FILE, "w", encoding="utf-8-sig", newline='') as authors_file:
        writer = csv.DictWriter(authors_file, fieldnames=AUTHORS_HEADER)
        writer.writeheader()

        for author_id, data in sorted(autores.items()):
            writer.writerow({
                'author_id': author_id,
                'artist_name': data['artist_name'],
                'artist_nacionality': data['artist_nacionality'],
                'album_title': str(data['album_title']),
                'rights_percentage': data['rights_percentage'],
                'total_earned': data['total_earned'],
            })

    print("Autores salvos com sucesso")


def save_albuns(albuns):
    """Grava os álbuns no CSV."""
    if not albuns:
        print('Não existem albuns para salvar')
        return

    with open(ALBUMS_FILE, "w", encoding="utf-8-sig", newline='') as albums_file:
        writer = csv.DictWriter(albums_file, fieldnames=ALBUMS_HEADER)
        writer.writeheader()

        for album_id, data in sorted(albuns.items()):
            writer.writerow({
                'album_id': album_id,
                'album_title': data['album_title'],
                'artist_name': data['artist_name'],
                'album_genere': data['album_genere'],
                'album_date': data['album_date'],
                'unites_sold': data['unites_sold'],
                'album_price': data['album_price'],
                'tracks': str(data['tracks']),
            })

    print("Álbuns salvos com sucesso")


def save_musicas(musicas):
    """Grava músicas no CSV usando pandas."""
    if not musicas:
        print('Não existem músicas para salvar')
        return

    df = pd.DataFrame(musicas)
    df.to_csv(TRACKS_FILE, index=False, encoding="utf-8-sig")
    print("Músicas salvas com sucesso")


# ====================== OPERAÇÕES CRUD ======================

def adicionar_autor():
    """
    Adiciona um novo autor ao sistema.
    Faz validação, cria snapshot e atualiza o índice de pesquisa.
    """

    autores = load_autores()

    nome = input("Nome do autor: ").strip()
    if not nome:
        print("Nome do autor inválido.")
        return

    # Evita duplicados
    if any(a['artist_name'].lower() == nome.lower() for a in autores.values()):
        print('Autor já existe')
        return

    nac = input("Nacionalidade: ").strip()

    try:
        direitos = float(input("Percentagem de direitos (0-100): "))
        if not 0 <= direitos <= 100:
            print("Percentagem inválida.")
            return
    except ValueError:
        print("Percentagem inválida (0-100).")
        return

    novo_id = max(autores.keys(), default=0) + 1

    novo_autor = {
        "artist_name": nome,
        "artist_nacionality": nac,
        "album_title": [],
        "rights_percentage": direitos,
        "total_earned": 0.0
    }

    # Validação com schema
    try:
        dS.authorsSchema.validate({novo_id: novo_autor})
    except Exception as e:
        print(f"Validação falhou: {e}")
        return

    autores[novo_id] = novo_autor

    salvar_snapshot(f"Adicionado autor '{nome}'")
    save_autores(autores)
    build_unified_index()

    print("Autor adicionado com sucesso!")


def remover_autor(nome):
    """
    Remove um autor pelo nome.
    Faz cascade delete: remove autor, álbuns e músicas associadas.
    Cria snapshot e atualiza índice.
    """

    autores = load_autores()
    chave = next((k for k, a in autores.items() if a["artist_name"].lower() == nome.lower()), None)

    if not chave:
        print("Autor não encontrado")
        return

    confirm = input(f"Confirma remoção do autor '{nome}' (s/n): ").lower()
    if confirm != 's':
        print("Operação cancelada")
        return

    del autores[chave]

    # Remoção dos álbuns do autor
    albuns = load_albuns()
    albuns_to_remove = {k for k, v in albuns.items() if v['artist_name'].lower() == nome.lower()}
    for alb_id in albuns_to_remove:
        del albuns[alb_id]

    # Remoção das músicas do autor
    musicas = load_musicas()
    musicas = [m for m in musicas if m['artist_name'].lower() != nome.lower()]

    salvar_snapshot(f"Removido autor '{nome}' (ID {chave}) + álbuns e faixas relacionados")

    save_autores(autores)
    save_albuns(albuns)
    save_musicas(musicas)

    build_unified_index()

    print(f"Autor '{nome}' removido com sucesso")


def atualizar_direitos_autor(nome, nova_percentagem):
    """
    Atualiza a percentagem de direitos de um autor.
    Valida o intervalo e cria snapshot antes de gravar.
    """

    autores = load_autores()
    chave = next((k for k, a in autores.items() if a["artist_name"].lower() == nome.lower()), None)

    if not chave:
        print("Autor não encontrado")
        return

    try:
        if not 0 <= nova_percentagem <= 100:
            raise ValueError
        autores[chave]['rights_percentage'] = nova_percentagem
    except ValueError:
        print("Percentagem inválida (0-100)")
        return

    salvar_snapshot(f"Atualizada percentagem de direitos de '{nome}' para {nova_percentagem}%")
    save_autores(autores)
    build_unified_index()

    print(f"Direitos atualizados para {nova_percentagem}%")