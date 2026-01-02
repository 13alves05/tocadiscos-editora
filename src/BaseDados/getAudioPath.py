def getAudioPath(track_id):
    path = 'data/songs/'

    track_id = str(track_id)
    if len(track_id) < 6:
        missing = 6 - len(track_id)
        for x in range(missing):
            track_id = '0' + track_id

    path += track_id[0:3] + '/' + track_id[3:len(track_id)]


    return path