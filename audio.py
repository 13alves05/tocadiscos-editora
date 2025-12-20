"""
Localização e reprodução de ficheiros áudio,
usei getAudioPath(track_id) para construir caminhos,
usei load_musicas() do crud para procurar metadados,
interface de reprodução simples via terminal
"""

import os  # para verificar existência de ficheiros
from typing import Optional  # para anotações de tipos
import pygame  # biblioteca para reprodução de áudio
from crud import load_musicas  # para carregar metadados das músicas
from getAudioPath import getAudioPath  # para construir caminhos de ficheiros áudio

def init_audio():
    # inicializo o mixer do pygame
    pygame.mixer.init()

def encontrar_caminho_musica(titulo_track, titulo_album=None):
    # procuro a música pelo título
    musicas = load_musicas()

    for m in musicas:

        if m["track_title"].lower() == titulo_track.lower() and (not titulo_album or m["album_title"].lower() == titulo_album.lower()):

            caminho = getAudioPath(m["track_id"]) + ".mp3"

            if os.path.exists(caminho):

                return caminho
            
            print(f"Debug: ficheiro não encontrado - {caminho}")  # print para depurar

    return None

def reproduzir_musica(titulo_track, titulo_album=None):
    # reproduzo a música
    init_audio()
    caminho = encontrar_caminho_musica(titulo_track, titulo_album)

    if not caminho:

        return "Música não encontrada ou ficheiro inexistente"
    
    try:

        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()

        print(f"Reproduzindo {titulo_track}... (Enter pausa/resume, s para parar, q para sair)")

        pausado = False

        while True:

            cmd = input().strip().lower()

            if cmd == "":

                if pausado:

                    pygame.mixer.music.unpause()
                    pausado = False

                else:

                    pygame.mixer.music.pause()
                    pausado = True

            elif cmd == "s":

                pygame.mixer.music.stop()
                break

            elif cmd == "q":

                pygame.mixer.music.stop()

                return "Reprodução terminada"
            
    except Exception as e:

        return f"Erro na reprodução: {e}"

if __name__ == "__main__":
    
    print(reproduzir_musica("Food"))  # teste com uma música do CSV