"""
Localização e reprodução de ficheiros áudio.
Usa getAudioPath(track_id) para construir caminhos,
load_musicas() para obter metadados,
e pygame para reprodução de áudio.
"""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  
# Esta linha serve apenas para esconder a mensagem chata do pygame quando inicia.

import pygame
import crud
from BaseDados.getAudioPath import getAudioPath


def encontrar_caminho_musica(titulo_track, titulo_album=None):
    """
    Procura o caminho do ficheiro de áudio a partir do título da música.
    Se for passado também o título do álbum, filtra ainda mais a pesquisa.
    """

    # Carregamos todas as músicas já processadas pelo sistema.
    musicas = crud.load_musicas()

    encontrou_no_csv = False  # Flag para sabermos se a música existe nos dados.

    # Percorremos todas as músicas à procura de uma correspondência.
    for m in musicas:

        # Comparação case-insensitive do título da música.
        if m["track_title"].strip().lower() == titulo_track.strip().lower():

            # Se o utilizador indicou álbum, também verificamos isso.
            if not titulo_album or m["album_title"].strip().lower() == titulo_album.strip().lower():

                # Construímos o caminho usando o track_id e adicionamos a extensão .mp3.
                caminho = getAudioPath(m["track_id"]) + ".mp3"
                encontrou_no_csv = True

                # Verificamos se o ficheiro existe mesmo no disco.
                if os.path.exists(caminho):
                    return caminho
                else:
                    print("Esta música não está adicionada.")

    # Se nunca encontrámos a música no CSV, avisamos o utilizador.
    if not encontrou_no_csv:
        print("Música não existe.")

    return


def init_audio():
    # Inicializa o mixer do pygame apenas se ainda não estiver inicializado.
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def play_music(path):
    # Carrega e toca a música indicada pelo caminho.
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except:
        print("Não foi possível tocar a música.")


def pause_music():
    # Pausa a música atual.
    try:
        pygame.mixer.music.pause()
    except:
        print("Não foi possível pausar.")


def resume_music():
    # Retoma a música pausada.
    try:
        pygame.mixer.music.unpause()
    except:
        print("Não foi possível voltar a música.")


def stop_music():
    # Para completamente a reprodução.
    try:
        pygame.mixer.music.stop()
    except:
        print("Não foi possível parar a música.")


def is_playing():
    # Retorna True se alguma música estiver a tocar.
    return pygame.mixer.music.get_busy()