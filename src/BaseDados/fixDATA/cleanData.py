
## NACIONALIDADE ##
import random

def atribuir_nacionalidade ():
    nacionalidades = [
        "Português",
        "Brasileiro",
        "Espanhol",
        "Francês",
        "Alemão",
        "Italiano",
        "Inglês",
        "Americano",
        "Japonês",
        "Chinês",
        "Indiano",
        "Russo",
        "Mexicano",
        "Canadiano",
        "Australiano"
    ]

    indice = random.randint(0, len(nacionalidades)-1)

    return nacionalidades[indice]
## ----FIM---- NACIONALIDADE ##



## PREÇO  TRACK ##
def atribuir_preco_track():
    return round( random.uniform(0.70, 1.4) ,2)
## ----FIM---- PREÇO A TRACK ##




## CLEAN DATA ##

tracksRaw = open('data/raw_tracks.csv', 'r', encoding='utf-8-sig' )
tracksRawData = tracksRaw.readlines()
tracksRaw.close()

cleanRawData = []

campos = tracksRawData[0].replace('\n','').split(',')
campos.append('artist_nacionality')
campos.append('track_price\n')
cleanRawData.append(','.join(campos))

## adding clean and formated data to cleanRawData
indexOfGenre = campos.index('track_genres')

for line in tracksRawData[1:]: 

    try:
        int(line[0])
    except:
        continue

    line = line.replace('\n','').split(',')
    line.append(atribuir_nacionalidade())
    line.append(str(atribuir_preco_track()) + '\n')

    if len(line) < len(campos) or len(line) > len(campos) :
        continue
    else:
        ## finding genre of track
        genreCampoArray = line[indexOfGenre].split(',')

        for item in genreCampoArray:
            if 'genre_title' in item:
                line[indexOfGenre] = item[item.find(':') + 3: len(item)-1]
        # ## ----FIM---- finding genre of track


        cleanRawData.append(','.join(line))

## override clean data to raw_tracks
tracksRaw = open('data/raw_tracks.csv', 'w', encoding='utf-8-sig' )
tracksRaw.writelines(cleanRawData)
tracksRaw.close()

## ----FIM---- CLEAN DATA ##