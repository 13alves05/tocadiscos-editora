def getAudioPath(track_id):
    # Caminho base onde estão guardadas as músicas
    path = 'data/songs/'

    # Convertimos o track_id para string para podermos manipular os dígitos
    track_id = str(track_id)

    # O sistema de pastas usa IDs com 6 dígitos.
    # Se o ID tiver menos de 6 dígitos, adicionamos zeros à esquerda.
    if len(track_id) < 6:
        missing = 6 - len(track_id)
        for x in range(missing):
            track_id = '0' + track_id

    # A estrutura das pastas é:
    #   data/songs/XXX/XXXXXX
    # Onde:
    #   - XXX são os primeiros 3 dígitos do ID
    #   - XXXXXX é o ID completo com zeros à esquerda
    path += track_id[0:3] + '/' + track_id[0:len(track_id)]

    # Devolvemos o caminho final para o ficheiro áudio
    return path