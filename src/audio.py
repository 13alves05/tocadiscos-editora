"""
Localização e reprodução de ficheiros áudio.
Usa getAudioPath(track_id) para construir caminhos,
load_musicas() para obter metadados,
e pygame para reprodução de áudio.
"""

import os
import pygame
from crud import load_musicas
from BaseDados.getAudioPath import getAudioPath

# Estado global do áudio
_audio_inicializado = False


def init_audio():
    """Inicializa o sistema de áudio (apenas uma vez)."""
    global _audio_inicializado
    if not _audio_inicializado:
        pygame.init()
        pygame.mixer.init()
        _audio_inicializado = True


def encontrar_caminho_musica(titulo_track, titulo_album=None):
    """
    Procura o caminho do ficheiro de áudio a partir do título da música.
    Pode opcionalmente filtrar por álbum.
    """
    musicas = load_musicas()

    for m in musicas:
        if m["track_title"].lower() == titulo_track.lower():
            if not titulo_album or m["album_title"].lower() == titulo_album.lower():
                caminho = getAudioPath(m["track_id"]) + ".mp3"

                if os.path.exists(caminho):
                    return caminho
                else:
                    print(f"Debug: ficheiro não encontrado -> {caminho}")

    return None


def reproduzir_musica(titulo_track, titulo_album=None):
    """
    Reproduz uma música via terminal.
    Controlo:
      ENTER → pausa/retoma
      s     → parar
      q     → sair
    """
    init_audio()

    caminho = encontrar_caminho_musica(titulo_track, titulo_album)
    if not caminho:
        return "Música não encontrada ou ficheiro inexistente."

    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()

        print(f"\n🎵 A reproduzir: {titulo_track}")
        print("ENTER = pausa/retomar | s = parar | q = sair")

        pausado = False

        while True:
            comando = input().strip().lower()

            if comando == "":
                if pausado:
                    pygame.mixer.music.unpause()
                    pausado = False
                else:
                    pygame.mixer.music.pause()
                    pausado = True

            elif comando == "s":
                pygame.mixer.music.stop()
                break

            elif comando == "q":
                pygame.mixer.music.stop()
                return "Reprodução terminada."

    except Exception as e:
        return f"Erro na reprodução: {e}"