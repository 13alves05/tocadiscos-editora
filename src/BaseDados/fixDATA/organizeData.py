from csv import DictReader
from random import randint

## MAKING DIFFERENT TABLES ##
authorsData = []
albumsData = []

authorsDict = {}
albumsDict = {}

tracksUsableFile = open('data/raw_tracks.csv', 'r', encoding='utf-8-sig' )
tracksUsableData = list(DictReader(tracksUsableFile.readlines())) # transforma cada linha numa lista
tracksUsableFile.close()


## organize data into authors and albums tables

for linha in tracksUsableData[1:4]:    

    ##adicionar nova entrada em autor e albums se não existir
    if len(authorsDict) == 0 and len(albumsDict) == 0 or len(authorsDict) > 0 and len(albumsDict) > 0 and linha['artist_id'] not in authorsDict.get() and linha['album_id'] not in albumsDict.get():

        authorsDict[linha['artist_id']] = {
            'artist_name' : linha['artist_name'],
            'artist_nacionality' :linha['artist_nacionality'],
            'album_title': [linha['album_title']],
            'rights_percentage' : randint(30, 50),
            'total_earned' : linha['track_price']
        }

        albumsDict[linha['album_id']] = {
            'album_title': linha['album_title'],
            'artist_name': linha['artist_name'],
            'album_genere': linha['track_genres'],
            'album_date': linha['track_date_recorded'],
            'unites_sold': linha['track_interest'],
            'album_price': linha['track_price'],
            'tracks': [(linha['track_id'],linha['track_title'])],
            
        }
        
#     else:


# print(albumsDict)
# print(authorsDict)


## creating authors table

# authorsTable = open('data/authors_table.csv', 'w', encoding='utf-8-sig')
# authorsTable.writelines()
# authorsTable.close()


## creating albums table

# albumsTable = open('data/albums_table.csv', 'w', encoding='utf-8-sig')
# albumsTable.writelines()
# albumsTable.close()


## ----FIM---- MAKING DIFFERENT TABLES ##