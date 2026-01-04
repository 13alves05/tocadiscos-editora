"""
Localização e reprodução de ficheiros áudio.
Usa getAudioPath(track_id) para construir caminhos,
load_musicas() para obter metadados,
e pygame para reprodução de áudio.
"""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import crud
from BaseDados.getAudioPath import getAudioPath

def encontrar_caminho_musica(titulo_track, titulo_album=None):
    
    "Procura o caminho do ficheiro de áudio a partir do título da música. Pode opcionalmente filtrar por álbum."
    musicas = crud.load_musicas()

    encontrou_no_csv = False

    for m in musicas:
        if m["track_title"].strip().lower() == titulo_track.strip().lower():
            if not titulo_album or m["album_title"].strip().lower() == titulo_album.strip().lower():
                caminho = getAudioPath(m["track_id"]) + ".mp3"
                encontrou_no_csv = True

                if os.path.exists(caminho):
                    return caminho
                else:
                    print("Esta música não está adicionada.")
    
    if not encontrou_no_csv:
        print("Música não existe.")

    return

def init_audio():
    if not pygame.mixer.get_init():
        pygame.mixer.init()

def play_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except:
        print("Não foi possível tocar a música.")

def pause_music():
    try:
        pygame.mixer.music.pause()
    except:
        print("Não foi possível pausar.")

def resume_music():
    try:
        pygame.mixer.music.unpause()
    except:
        print("Não foi possível votlar a música.")

def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        print("Não foi possível parar a música.")

def is_playing():
    return pygame.mixer.music.get_busy()