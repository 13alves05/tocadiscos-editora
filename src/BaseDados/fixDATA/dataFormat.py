from random import randint

def feedAuthors (authorsDict, line):
    authorsDict[int(line['artist_id'])] = {
                    'artist_name' : line['artist_name'],
                    'artist_nacionality' :line['artist_nacionality'],
                    'album_title': [(int(line['album_id']), line['album_title'])],
                    'rights_percentage' : randint(10, 50),
                    'total_earned' : round(float(line['track_price']) * int(line['track_interest']),2)
                }


def updateAuthors(authorsDict, line):
    authorsDict[int(line['artist_id'])]['album_title'].append((int(line['album_id']), line['album_title']))
    authorsDict[int(line['artist_id'])]['total_earned'] += round(float(line['track_price']) * int(line['track_interest']),2)



def feedAlbums (albumsDict, line):
    albumsDict[int(line['album_id'])] = {
                    'album_title': line['album_title'],
                    'artist_name': line['artist_name'],
                    'album_genere': line['track_genres'],
                    'album_date': line['track_date_recorded'],
                    'unites_sold': int(line['track_interest']),
                    'album_price': float(line['track_price']),
                    'tracks': [(int(line['track_id']),line['track_title'])],
                }


def updateAlbums(albumsDict, line):

    #update unidades vendidas
    albumsDict[int(line['album_id'])]['unites_sold'] += int(line['track_interest'])

    #update preço album
    albumsDict[int(line['album_id'])]['album_price'] += float(line['track_price'])

    #update tracks
    albumsDict[int(line['album_id'])]['tracks'].append((int(line['track_id']),line['track_title'])) 



# def feedAuthentication():
