from csv import DictReader
from dataFormat import feedAlbums, updateAlbums, feedAuthors, updateAuthors

## MAKING DIFFERENT TABLES ##
authorsData = []
albumsData = []

authorsDict = {}
albumsDict = {}

tracksUsableFile = open('data/raw_tracks.csv', 'r', encoding='utf-8-sig' )
tracksUsableData = list(DictReader(tracksUsableFile.readlines())) # transforma cada line numa lista
tracksUsableFile.close()


## organize data into authors and albums tables

for line in tracksUsableData[1:]:

    emptyCount = 0

    for item in line.values():
        if item == '':
            emptyCount += 1

    if emptyCount > 0:
        print(line)
        continue


    # Inicializar o dicionário
    if len(authorsDict) == 0 and len(albumsDict) == 0:
        feedAuthors(authorsDict, line)
        feedAlbums(albumsDict, line) 
        print(authorsDict)

    # Adicionar novas entradas OU atualizar entradas existentes
    if len(authorsDict) > 0 and len(albumsDict) > 0:

        # Authors
        # Adicionar novo Autor
        if  int(line['artist_id']) not in authorsDict:
            try:
                feedAuthors(authorsDict, line)
            except:
                continue

        # Adicionar dados a autor já existente
        elif int(line['artist_id'])  in authorsDict:
            try:
                updateAuthors(authorsDict, line)
            except:
                continue


        # Albums
        # Adicionar novo album
        if int(line['album_id']) not in albumsDict:
            try:
                feedAlbums(albumsDict, line)
            except:
                continue


        # Adicionar dados a a album já existente
        elif int(line['album_id']) not in albumsDict:
            try:
                updateAlbums(albumsDict)
            except:
                continue


print(authorsDict)

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