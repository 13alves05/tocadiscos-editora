"""
Operações de I/O para os ficheiros CSV autores, álbuns, músicas,
fiz funções de carregamento e gravação, funções para adicionar/remover autores com integração com history.salvar_snapshot
"""

import ast  # para converter strings de listas em listas reais
from history import salvar_snapshot  # chamo esta função para guardar snapshot
import pandas as pd  # para ler e escrever o raw_tracks.csv que é grande
import os  # para criar pastas se necessário
import BaseDados.dataSchema as dS  # Schemas de validação (opcional)

def load_autores():
    """
    Carrega os autores do CSV para um dicionário em memória.
    Usa parsing manual para listas de álbuns.
    """
    autores = {}

    with open("data/authors_table.csv", "r", encoding="utf-8-sig") as f:

        for linha in f.readlines()[1:]:  # salto o cabeçalho
            partes = linha.strip().split(",")

            id_ = int(partes[0])
            nome = partes[1]
            nac = partes[2]
            # juntamos as partes do meio para a lista de álbuns
            album_str = ",".join(partes[3:-2])
            direitos = float(partes[-2])
            ganho = float(partes[-1])

            # converte string de lista para lista real
            try:
                albuns = ast.literal_eval(album_str)
            except:
                albuns = []

            autores[id_] = {
                "artist_name": nome,
                "artist_nacionality": nac,
                "album_title": albuns,
                "rights_percentage": direitos,
                "total_earned": ganho
            }

    print(f"Debug: carreguei {len(autores)} autores")  # print para depurar
    return autores


def save_autores(autores):
    """
    Salva o dicionário de autores no CSV correspondente.
    """
    with open("data/authors_table.csv", "w", encoding="utf-8-sig") as f:
        f.write("author_id,artist_name,artist_nacionality,album_title,rights_percentage,total_earned\n")
        for id_, a in autores.items():
            f.write(f"{id_},{a['artist_name']},{a['artist_nacionality']},{a['album_title']},{a['rights_percentage']},{a['total_earned']}\n")

    print("Autores salvos com sucesso")  # print para depurar


def load_albuns():
    """
    Carrega os álbuns do CSV para um dicionário em memória.
    Converte listas de tracks de string para lista real.
    """
    albuns = {}

    with open("data/albums_table.csv", "r", encoding="utf-8-sig") as f:

        for linha in f.readlines()[1:]:  # salto o cabeçalho
            partes = linha.strip().split(",")

            id_ = int(partes[0])
            titulo = partes[1]
            artista = partes[2]
            genero = partes[3]
            data = partes[4]
            vendas = int(partes[5])
            preco = float(partes[6])
            tracks_str = ",".join(partes[7:])
            try:
                tracks = ast.literal_eval(tracks_str)
            except:
                tracks = []

            albuns[id_] = {
                "album_title": titulo,
                "artist_name": artista,
                "album_genere": genero,
                "album_date": data,
                "unites_sold": vendas,
                "album_price": preco,
                "tracks": tracks
            }

    print(f"Debug: carreguei {len(albuns)} álbuns")  # print para depurar
    return albuns


def save_albuns(albuns):
    """
    Salva o dicionário de álbuns no CSV correspondente.
    """
    with open("data/albums_table.csv", "w", encoding="utf-8-sig") as f:
        f.write("album_id,album_title,artist_name,album_genere,album_date,unites_sold,album_price,tracks\n")
        for id_, alb in albuns.items():
            f.write(f"{id_},{alb['album_title']},{alb['artist_name']},{alb['album_genere']},{alb['album_date']},{alb['unites_sold']},{alb['album_price']},{alb['tracks']}\n")

    print("Álbuns salvos com sucesso")  # print para depurar


def load_musicas():
    """
    Carrega músicas usando pandas para performance em ficheiros grandes.
    """
    df = pd.read_csv("data/raw_tracks.csv", encoding="utf-8-sig")
    musicas = df.to_dict(orient="records")
    print(f"Debug: carreguei {len(musicas)} músicas")  # print para depurar
    return musicas


def save_musicas(musicas):
    """
    Salva a lista de músicas no CSV usando pandas.
    """
    df = pd.DataFrame(musicas)
    df.to_csv("data/raw_tracks.csv", index=False, encoding="utf-8-sig")
    print("Músicas salvas com sucesso")  # print para depurar


def adicionar_autor():
    """
    Adiciona um novo autor ao sistema:
    - Atualiza CSV
    - Cria snapshot no histórico
    - Inicializa álbuns vazios
    """
    autores = load_autores()

    nome = input("Nome do autor: ").strip()

    if any(a["artist_name"].lower() == nome.lower() for a in autores.values()):
        return "Autor já existe"

    nac = input("Nacionalidade: ").strip()

    try:
        direitos = float(input("Percentagem de direitos (0-100): "))
        if not 0 <= direitos <= 100:
            return "Percentagem inválida"
    except:
        return "Entrada inválida para percentagem"

    novo_id = max(autores.keys()) + 1 if autores else 1
    autores[novo_id] = {
        "artist_name": nome,
        "artist_nacionality": nac,
        "album_title": [],
        "rights_percentage": direitos,
        "total_earned": 0.0
    }

    salvar_snapshot(f"Adicionado {nome}")  # guardo snapshot antes de salvar
    save_autores(autores)

    print("Autor adicionado")  # print para depurar
    return "Autor adicionado com sucesso"


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