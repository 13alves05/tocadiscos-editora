"""
Operações de I/O para os ficheiros CSV autores, álbuns, músicas.
Funções de carregamento, gravação, adicionar/remover autores com integração com history.salvar_snapshot.
"""
import csv
import ast
from pathlib import Path
import pandas as pd
from history import salvar_snapshot

# Caminhos dos ficheiros
AUTHORS_FILE = Path("data/authors_table.csv")
ALBUMS_FILE = Path("data/albums_table.csv")
TRACKS_FILE = Path("data/raw_tracks.csv")

# Headers das Tabelas
AUTHORS_HEADER = ['author_id','artist_name','artist_nacionality','album_title','rights_percentage','total_earned']
ALBUMS_HEADER = ['album_id','album_title','artist_name','album_genere','album_date','unites_sold','album_price','tracks']
TRACKS_HEADER = ['track_id','album_id','album_title','artist_id','artist_name','track_date_recorded','track_genres','track_interest','track_number','track_title','artist_nacionality','track_price','artist_nacionality','track_price']

# ====================== CARREGAMENTO SEGURO ======================

def load_autores():
    """Carrega autores, parse album_title list"""
    autores = {}

    if not AUTHORS_FILE.exists():
        return autores

    with open(AUTHORS_FILE, "r", encoding="utf-8-sig") as authors_file:
        reader = csv.DictReader(authors_file)
        for row in reader:
            try:
                author_id = int(row['author_id'])
                album_str = row.get('album_title', '[]')

                try:
                    albums_list = ast.literal_eval(album_str)
                    if not isinstance(albums_list, list):
                        albums_list = []
                except:
                    albums_list = []

                # Guardamos o dicionário completo, mas com album_title já parseado
                row_copy = row.copy()
                row_copy['album_title'] = albums_list
                autores[author_id] = row_copy
            except (ValueError, KeyError):
                continue  # ignora linhas inválidas
    
    print(f"Debug: carreguei {len(autores)} autores")
    return autores


def load_albuns():
    """Carrega álbuns, parseando a lista de tracks"""
    albuns = {}
    if not ALBUMS_FILE.exists():
        return albuns

    with open(ALBUMS_FILE, "r", encoding="utf-8-sig") as albums_file:
        reader = csv.DictReader(albums_file)
        for row in reader:
            try:
                album_id = int(row['album_id'])
                tracks_str = row.get('tracks', '[]')

                try:
                    tracks_list = ast.literal_eval(tracks_str)
                    if not isinstance(tracks_list, list):
                        tracks_list = []
                except:
                    tracks_list = []

                # Guardamos o dicionário completo do álbum
                row_copy = row.copy()
                row_copy['tracks'] = tracks_list
                albuns[album_id] = row_copy

            except (ValueError, KeyError):
                continue

    print(f"Debug: carreguei {len(albuns)} álbuns")
    return albuns


def load_musicas():
    """Carrega músicas usando pandas para maior robustez"""
    if not TRACKS_FILE.exists():
        return []

    df = pd.read_csv(TRACKS_FILE, encoding="utf-8-sig", keep_default_na=False)
    musicas = df.to_dict(orient="records")

    print(f"Debug: carreguei {len(musicas)} músicas")
    return musicas


# ====================== GRAVAÇÃO SEGURA ======================

def save_autores(autores_dict):
    """Grava autores no CSV"""
    if not autores_dict:
        print("Não existem autores para salvar.")
        return

    autores_list = []
    for author_id, data in sorted(autores_dict.items(), key=lambda x: x[0]):
        autores_list.append({
            'author_id': author_id,
            'artist_name': data['artist_name'],
            'artist_nacionality': data['artist_nacionality'],
            'album_title': str(data['album_title']),  # converte lista para string
            'rights_percentage': data['rights_percentage'],
            'total_earned': data['total_earned'],
        })

    with open(AUTHORS_FILE, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=AUTHORS_HEADER)
        writer.writeheader()
        writer.writerows(autores_list)

    salvar_snapshot("Atualizado authors_table.csv")
    print("Autores salvos com sucesso.")


def save_albuns(albuns_dict):
    """Grava álbuns no CSV"""
    if not albuns_dict:
        print("Não existem álbuns para salvar.")
        return

    albuns_list = []
    for album_id, data in sorted(albuns_dict.items(), key=lambda x: x[0]):
        albuns_list.append({
            'album_id': album_id,
            'album_title': data['album_title'],
            'artist_name': data['artist_name'],
            'album_genere': data['album_genere'],
            'album_date': data['album_date'],
            'unites_sold': data['unites_sold'],
            'album_price': data['album_price'],
            'tracks': str(data['tracks']),  # converte lista para string
        })

    with open(ALBUMS_FILE, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=ALBUMS_HEADER)
        writer.writeheader()
        writer.writerows(albuns_list)

    salvar_snapshot("Atualizado albums_table.csv")
    print("Álbuns salvos com sucesso.")


def save_musicas(musicas_list):
    """Grava músicas no CSV usando pandas"""
    if not musicas_list:
        print("Não existem músicas para salvar.")
        return

    pd.DataFrame(musicas_list).to_csv(TRACKS_FILE, index=False, encoding="utf-8")
    salvar_snapshot("Atualizado raw_tracks.csv")
    print("Músicas salvas com sucesso.")


# ====================== OPERAÇÕES CRUD ======================

def adicionar_autor():
    """Adiciona um novo autor com validação e snapshot."""
    autores = load_autores()

    nome = input("Nome do autor: ").strip()
    if any(a["artist_name"].lower() == nome.lower() for a in autores.values()):
        print("Autor já existe.")
        return

    nac = input("Nacionalidade: ").strip()
    try:
        direitos = float(input("Percentagem de direitos (0-100): "))
        if not 0 <= direitos <= 100:
            print("Percentagem inválida.")
            return
    except ValueError:
        print("Valor inválido para percentagem.")
        return

    novo_id = max(autores.keys(), default=0) + 1
    autores[novo_id] = {
        "artist_name": nome,
        "artist_nacionality": nac,
        "album_title": [],
        "rights_percentage": direitos,
        "total_earned": 0.0
    }

    save_autores(autores)
    print("Autor adicionado com sucesso!")


def remover_autor(nome):
    """Remove um autor e tudo relacionado"""
    autores = load_autores()
    chave = next((k for k, a in autores.items() if a["artist_name"].lower() == nome.lower()), None)

    if not chave:
        print("Autor não encontrado.")
        return

    if input("Confirma remoção (s/n): ").lower() != "s":
        print("Operação cancelada.")
        return

    # Remove autor
    del autores[chave]

    # Remove álbuns do autor
    albuns = load_albuns()
    albuns = {k: v for k, v in albuns.items() if v["artist_name"].lower() != nome.lower()}
    save_albuns(albuns)

    # Remove músicas do autor
    musicas = load_musicas()
    musicas = [m for m in musicas if m["artist_name"].lower() != nome.lower()]
    save_musicas(musicas)

    save_autores(autores)
    print("Autor removido com sucesso!")