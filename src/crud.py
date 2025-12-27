"""
Operações de I/O para os ficheiros CSV autores, álbuns, músicas,
fiz funções de carregamento e gravação, funções para adicionar/remover autores com integração com history.salvar_snapshot
"""

import ast  # para converter strings de listas em listas reais
from history import salvar_snapshot  # chamo esta função para guardar snapshot
import pandas as pd  # para ler e escrever o raw_tracks.csv que é grande
import os  # para criar pastas se necessário

def load_autores():
    # carrego autores do CSV com parsing manual
    autores = {}

    with open("data/authors_table.csv", "r", encoding="utf-8-sig") as f:

        for linha in f.readlines()[1:]:  # salto o cabeçalho

            partes = linha.strip().split(",")
            id_ = int(partes[0])
            nome = partes[1]
            nac = partes[2]
            album_str = ",".join(partes[3:-2])  # junto as partes do meio para a lista de álbuns
            direitos = float(partes[-2])
            ganho = float(partes[-1])
            albuns = ast.literal_eval(album_str)  # converto string para lista
            autores[id_] = {"artist_name": nome, "artist_nacionality": nac, "album_title": albuns, "rights_percentage": direitos, "total_earned": ganho}

    print(f"Debug: carreguei {len(autores)} autores")  # print para depurar

    return autores

def save_autores(autores):
    # salvo autores no CSV
    with open("data/authors_table.csv", "w", encoding="utf-8-sig") as f:

        f.write("author_id,artist_name,artist_nacionality,album_title,rights_percentage,total_earned\n")

        for id_, a in autores.items():

            f.write(f"{id_},{a['artist_name']},{a['artist_nacionality']},{a['album_title']},{a['rights_percentage']},{a['total_earned']}\n")

    print("Autores salvos")  # print para depurar

def load_albuns():
    # carrego álbuns com parsing manual
    albuns = {}

    with open("data/albums_table.csv", "r", encoding="utf-8-sig") as f:

        for linha in f.readlines()[1:]:

            partes = linha.strip().split(",")
            id_ = int(partes[0])
            titulo = partes[1]
            artista = partes[2]
            genero = partes[3]
            data = partes[4]
            vendidas = int(partes[5]) if partes[5] else 0
            preco = float(partes[6])
            tracks_str = ",".join(partes[7:])
            tracks = ast.literal_eval(tracks_str)
            albuns[id_] = {"album_title": titulo, "artist_name": artista, "album_genere": genero, "album_date": data, "unites_sold": vendidas, "album_price": preco, "tracks": tracks}

    print(f"Debug: carreguei {len(albuns)} álbuns")  # print para depurar

    return albuns

def save_albuns(albuns):
    # salvo álbuns no CSV
    with open("data/albums_table.csv", "w", encoding="utf-8-sig") as f:

        f.write("album_id,album_title,artist_name,album_genere,album_date,unites_sold,album_price,tracks\n")

        for id_, a in albuns.items():

            f.write(f"{id_},{a['album_title']},{a['artist_name']},{a['album_genere']},{a['album_date']},{a['unites_sold']},{a['album_price']},{a['tracks']}\n")

    print("Álbuns salvos")  # print para depurar

def load_musicas():
    # carrego músicas com pandas, é mais fácil
    df = pd.read_csv("data/raw_tracks.csv")

    return df.to_dict("records")

def save_musicas(musicas):
    # salvo músicas com pandas
    df = pd.DataFrame(musicas)

    df.to_csv("data/raw_tracks.csv", index=False, encoding="utf-8-sig")

    print("Músicas salvas")  # print para depurar

def adicionar_autor():
    # adiciono um novo autor
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
    autores[novo_id] = {"artist_name": nome, "artist_nacionality": nac, "album_title": [], "rights_percentage": direitos, "total_earned": 0.0}
    salvar_snapshot(f"Adicionado {nome}")  # guardo snapshot antes de salvar
    save_autores(autores)

    print("Autor adicionado")  # print para depurar

    return "Autor adicionado com sucesso"

def remover_autor(nome):
    # removo um autor e os seus álbuns/músicas
    autores = load_autores()
    chave = next((k for k, a in autores.items() if a["artist_name"].lower() == nome.lower()), None)

    if not chave:

        return "Autor não encontrado"
    
    if input("Confirma remoção (s/n): ").lower() != "s":

        return "Operação cancelada"
    
    del autores[chave] # remove o autor
    albuns = load_albuns()
    albuns = {k: v for k, v in albuns.items() if v["artist_name"].lower() != nome.lower()}
    save_albuns(albuns)
    musicas = load_musicas()
    musicas = [m for m in musicas if m["artist_name"].lower() != nome.lower()]
    save_musicas(musicas)
    salvar_snapshot(f"Removido {nome}")
    save_autores(autores)

    print("Autor removido")  # print para depurar

    return "Autor removido com sucesso"

if __name__ == "__main__":
    
    print(adicionar_autor())  # teste rápido