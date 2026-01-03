"""
Operações de I/O para os ficheiros CSV autores, álbuns, músicas.
Funções de carregamento, gravação, adicionar/remover autores com integração com history.salvar_snapshot.
Validação com schemas de BaseDados.dataSchema.
"""
import csv
import ast
import os
from pathlib import Path
import pandas as pd
from history import salvar_snapshot
from BaseDados import dataSchema as dS  # Usamos os schemas de validação

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
        authors_list = csv.DictReader(authors_file)
        for author in authors_list:
            try:
                author_id = int(author['author_id'])
                album_str = author.get('album_title', [])

                try:
                    albums_list = ast.literal_eval(album_str)
                    author['album_title'] = albums_list
                    if not isinstance(albums_list, list):
                        albums_list = []
                except:
                    albums_list = []
            
                autores[author_id] = author
            except:
                continue
    
    print(f"Debug: carreguei {len(autores)} álbuns")
    return autores


def load_albuns():
    """Carrega álbuns ignorando cabeçalho e linhas inválidas."""
    albuns = {}
    if not ALBUMS_FILE.exists():
        return albuns

    with open(ALBUMS_FILE, "r", encoding="utf-8-sig") as albums_file:
        albums_list = csv.DictReader(albums_file)
        for album in albums_list:
            try:
                album_id = int(album['album_id'])
                album_tracks = album['tracks']

                try:
                    tracks_list = ast.literal_eval(album_tracks)
                    album['tracks'] = tracks_list
                    if not isinstance(tracks_list, list):
                        album['tracks'] = []
                except:
                    album['tracks'] = []
                
                albuns[album_id] = tracks_list

            except:
                continue

    print(f"Debug: carreguei {len(albuns)} álbuns")
    return albuns


def load_musicas():
    """Carrega músicas"""
    if not TRACKS_FILE.exists():
        return []

    df = pd.read_csv(TRACKS_FILE, encoding="utf-8-sig", keep_default_na=False)
    musicas = df.to_dict(orient="records")

    print(f"Debug: carreguei {len(musicas)} músicas")
    return musicas


# ====================== GRAVAÇÃO SEGURA ======================

def save_autores(autores):
    if not autores:
        print("Não existem autores para Salvar")
        return

    """Grava autores sobrescrevendo o ficheiro."""
    with open(AUTHORS_FILE, "w", encoding="utf-8-sig", newline='') as authors_file:
        writer = csv.DictWriter(authors_file)
        writer.writerow(AUTHORS_HEADER)

        # 'author_id','artist_name','artist_nacionality','album_title','rights_percentage','total_earned'
        for author_id, data in sorted(autores.items()):
            albums_str = str(data['album_title'])
            writer.writerow([
                author_id,
                data['artist_name'],
                data['artist_nacionality'],
                albums_str,
                data['rights_percentage'],
                data['total_earned'],
            ])

    print("Autores salvos com sucesso")


def save_albuns(albuns):
    if not albuns:
        print('Não existem albuns para salvar')
        return

    """Grava álbuns sobrescrevendo o ficheiro."""
    with open(ALBUMS_FILE, "w", encoding="utf-8-sig", newline='') as albums_file:
        writer = csv.DictWriter(albums_file)
        writer.writerow(ALBUMS_HEADER)

# 'album_id','album_title','artist_name','album_genere','album_date','unites_sold','album_price','tracks'
        for album_id, data in sorted(albuns.items()):
            album_tracks = str(data['tracks'])
            writer.writerow([
                album_id,
                data['album_title'],
                data['artist_name'],
                data['album_genere'],
                data['album_date'],
                data['unites_sold'],
                data['album_price'],
                album_tracks,
            ])
    print("Álbuns salvos com sucesso")


def save_musicas(musicas):
    """Grava músicas sobrescrevendo o ficheiro."""
    pd.DataFrame(musicas).to_csv(TRACKS_FILE, index=False, encoding="utf-8-sig")
    print("Músicas salvas com sucesso")


# ====================== OPERAÇÕES CRUD ======================

def adicionar_autor():
    """Adiciona um novo autor com validação e snapshot."""
    autores = load_autores()

    nome = input("Nome do autor: ").strip()
    if nome.lower() in [a["artist_name"].lower() for a in autores.values()]:
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

    salvar_snapshot(f"Adicionado autor '{nome}'")
    save_autores(autores)
    print("Autor adicionado com sucesso!")


def remover_autor(nome):
    """
    Remove um autor do sistema:
    - Remove todos os álbuns e músicas relacionados
    - Atualiza CSV
    - Cria snapshot no histórico
    """
    autores = load_autores()

    chave = next((k for k, a in autores.items() if a["artist_name"].lower() == nome.lower()), None)

    if not chave:
        print("Autor não encontrado")

    if input("Confirma remoção (s/n): ").lower() != "s":
        print("Operação cancelada")

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

    # Snapshot histórico
    salvar_snapshot(f"Removido {nome}")
    save_autores(autores)

    print("Autor removido")  # print para depurar
    return "Autor removido com sucesso"