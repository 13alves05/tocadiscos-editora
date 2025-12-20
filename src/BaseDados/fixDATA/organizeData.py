from csv import DictReader
from dataFormat import feedAlbums, updateAlbums, feedAuthors, updateAuthors

#ORGANIZING DATA IN DICTIONARIES
authorsDict = {}
albumsDict = {}

# transforma cada line numa lista
tracksUsableFile = open('data/raw_tracks.csv', 'r', encoding='utf-8-sig' )
tracksUsableData = list(DictReader(tracksUsableFile.readlines())) 
tracksUsableFile.close()


## organize data into authors and albums tables

for line in tracksUsableData[1:]:

    # descartar entradas desnecessárias
    try:
        artist_id = int(line['artist_id'])
        album_id = int(line['album_id'])
    except:
        continue


    # Inicializar o dicionário
    if len(authorsDict) == 0 and len(albumsDict) == 0:
        feedAuthors(authorsDict, line)
        feedAlbums(albumsDict, line) 

    # Adicionar novas entradas OU atualizar entradas existentes
    if len(authorsDict) > 0 and len(albumsDict) > 0:

        # Authors
        # Adicionar novo Autor
        if  artist_id not in authorsDict:
            try:
                feedAuthors(authorsDict, line)
            except:
                continue

        # Adicionar dados a autor já existente
        elif artist_id in authorsDict:
            try:
                updateAuthors(authorsDict, line)
            except:
                continue


        # Albums
        # Adicionar novo album
        if album_id not in albumsDict:
            try:
                feedAlbums(albumsDict, line)
            except:
                continue


        # Adicionar dados a a album já existente
        elif album_id in albumsDict:
            try:
                updateAlbums(albumsDict, line)
            except:
                continue

# ----FIM----  ORGANIZING DATA IN DICTIONARIES



# MAKING DIFFERENT TABLES
authorsData = []
albumsData = []

authorsColumns = list(authorsDict[1].keys())
authorsColumns.insert(0, 'author_id')
albumsColumns = list(albumsDict[1].keys())
albumsColumns.insert(0, 'album_id')

def dict_2_array (dicionario, lista):
    for index in dicionario:
        entry = list(dicionario[index].values())

        for val in range(0,len(entry)):
            entry[val] = str(entry[val])
        entry.insert(0, str(index))
        entry = ','.join(entry) + '\n'

        lista.append(entry)
        

# dict_2_array(authorsDict)
dict_2_array(authorsDict, authorsData)
dict_2_array(albumsDict, albumsData)


#adding columns to the begining of the array 

authorsData.insert(0, ','.join(authorsColumns) + '\n')
albumsData.insert(0, ','.join(albumsColumns) + '\n')


## creating authors table

authorsTable = open('data/authors_table.csv', 'w', encoding='utf-8-sig')
authorsTable.writelines(authorsData)
authorsTable.close()


## creating albums table

albumsTable = open('data/albums_table.csv', 'w', encoding='utf-8-sig')
albumsTable.writelines(albumsData)
albumsTable.close()


# ----FIM----  MAKING DIFFERENT TABLES