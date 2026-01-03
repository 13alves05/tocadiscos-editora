"""
Operações de I/O para os ficheiros CSV autores, álbuns, músicas.
Funções de carregamento, gravação, adicionar/remover autores com integração com history.salvar_snapshot.
Validação com schemas de BaseDados.dataSchema.
"""

import ast
import os
import pandas as pd
from history import salvar_snapshot
from BaseDados import dataSchema as dS  # Usamos os schemas de validação

# Caminhos dos ficheiros
AUTHORS_FILE = "data/authors_table.csv"
ALBUMS_FILE = "data/albums_table.csv"
TRACKS_FILE = "data/raw_tracks.csv"


# ====================== CARREGAMENTO SEGURO ======================

def load_autores():
    """Carrega autores ignorando cabeçalho e linhas inválidas."""
    autores = {}
    if not os.path.exists(AUTHORS_FILE):
        return autores

    with open(AUTHORS_FILE, "r", encoding="utf-8-sig") as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.startswith("author_id")]

    for linha in linhas:
        partes = linha.split(",")
        if len(partes) < 6:
            continue

        try:
            id_ = int(partes[0])
            nome = partes[1]
            nac = partes[2]
            album_str = ",".join(partes[3:-2])
            direitos = float(partes[-2])
            ganho = float(partes[-1])

            albuns = []
            if album_str:
                try:
                    parsed = ast.literal_eval(album_str)
                    if isinstance(parsed, list):
                        albuns = parsed
                except:
                    pass  # deixa vazio se falhar

            autor_data = {
                "artist_name": nome,
                "artist_nacionality": nac,
                "album_title": albuns,
                "rights_percentage": direitos,
                "total_earned": ganho
            }

            # Validação
            dS.authorsSchema.validate({id_: autor_data})
            autores[id_] = autor_data

        except Exception:
            continue  # ignora linha problemática

    print(f"Debug: carreguei {len(autores)} autores")
    return autores


def load_albuns():
    """Carrega álbuns ignorando cabeçalho e linhas inválidas."""
    albuns = {}
    if not os.path.exists(ALBUMS_FILE):
        return albuns

    with open(ALBUMS_FILE, "r", encoding="utf-8-sig") as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.startswith("album_id")]

    for linha in linhas:
        partes = linha.split(",")
        if len(partes) < 8:
            continue

        try:
            id_ = int(partes[0])
            titulo = partes[1]
            artista = partes[2]
            genero = partes[3]
            data = partes[4]
            vendas = int(partes[5])
            preco = float(partes[6])
            tracks_str = ",".join(partes[7:])

            tracks = []
            if tracks_str:
                try:
                    parsed = ast.literal_eval(tracks_str)
                    if isinstance(parsed, list):
                        tracks = parsed
                except:
                    pass

            album_data = {
                "album_title": titulo,
                "artist_name": artista,
                "album_genere": genero,
                "album_date": data,
                "unites_sold": vendas,
                "album_price": preco,
                "tracks": tracks
            }

            dS.albumsSchema.validate({id_: album_data})
            albuns[id_] = album_data

        except Exception:
            continue

    print(f"Debug: carreguei {len(albuns)} álbuns")
    return albuns


def load_musicas():
    """Carrega músicas com pandas (seguro contra NaN)."""
    if not os.path.exists(TRACKS_FILE):
        return []

    df = pd.read_csv(TRACKS_FILE, encoding="utf-8-sig", keep_default_na=False)
    musicas = df.to_dict(orient="records")
    print(f"Debug: carreguei {len(musicas)} músicas")
    return musicas


# ====================== GRAVAÇÃO SEGURA ======================

def save_autores(autores):
    """Grava autores sobrescrevendo o ficheiro."""
    with open(AUTHORS_FILE, "w", encoding="utf-8-sig", newline='') as f:
        f.write("author_id,artist_name,artist_nacionality,album_title,rights_percentage,total_earned\n")
        for id_, autor in sorted(autores.items()):
            f.write(f"{id_},{autor['artist_name']},{autor['artist_nacionality']},{autor['album_title']},{autor['rights_percentage']},{autor['total_earned']}\n")
    print("Autores salvos com sucesso")


def save_albuns(albuns):
    """Grava álbuns sobrescrevendo o ficheiro."""
    with open(ALBUMS_FILE, "w", encoding="utf-8-sig", newline='') as f:
        f.write("album_id,album_title,artist_name,album_genere,album_date,unites_sold,album_price,tracks\n")
        for id_, album in sorted(albuns.items()):
            f.write(f"{id_},{album['album_title']},{album['artist_name']},{album['album_genere']},{album['album_date']},{album['unites_sold']},{album['album_price']},{album['tracks']}\n")
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
        return "Autor não encontrado"

    if input("Confirma remoção (s/n): ").lower() != "s":
        return "Operação cancelada"

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