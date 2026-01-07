from schema import Schema, And, Use
import re

# ====================== FUNÇÕES AUXILIARES DE VALIDAÇÃO ======================

def non_empty_str(value):
    # Garante que recebemos uma string válida e não vazia.
    # Se vier algo vazio ou só espaços, rejeitamos.
    if not value or not str(value).strip():
        raise ValueError("Tem de ser uma string não vazia")
    return str(value).strip()

def positive_int(value):
    # Converte o valor para inteiro e garante que é maior que zero.
    # Usado para IDs e campos que nunca podem ser zero ou negativos.
    try:
        i = int(value)
        if i <= 0:
            raise ValueError
        return i
    except:
        raise ValueError(f"{value} tem de ser um inteiro positivo")

def non_negative_int(value):
    # Igual ao anterior, mas permite zero.
    # Usado para contagens como unidades vendidas.
    try:
        i = int(value)
        if i < 0:
            raise ValueError
        return i
    except:
        raise ValueError(f"{value} tem de ser um inteiro não negativo")

def positive_float(value):
    # Converte para float e garante que é maior que zero.
    # Usado para preços e valores monetários.
    try:
        f = float(value)
        if f <= 0:
            raise ValueError
        return f
    except:
        raise ValueError(f"{value} tem de ser um número positivo")

def non_negative_float(value):
    # Igual ao anterior, mas permite zero.
    # Usado para valores acumulados como total_earned.
    try:
        f = float(value)
        if f < 0:
            raise ValueError
        return f
    except:
        raise ValueError(f"{value} tem de ser um número não negativo")

def valid_date(value):
    # Verifica se a data está no formato YYYY-MM-DD.
    # Não valida se a data existe mesmo, só o formato.
    s = str(value)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        raise ValueError(f"{s} não é uma data válida (deve ser YYYY-MM-DD)")
    return s

def valid_genres(value):
    # Aceita um género musical como string única
    # ou uma lista de géneros (cada um não vazio).
    if isinstance(value, str):
        if value.strip():
            return value.strip()
        raise ValueError("Género musical não pode ser vazio")

    elif isinstance(value, list):
        # Lista tem de ter pelo menos um género
        # e todos têm de ser strings válidas.
        if len(value) > 0 and all(isinstance(g, str) and g.strip() for g in value):
            return [g.strip() for g in value]
        raise ValueError("Lista de géneros inválida ou vazia")

    else:
        raise ValueError("track_genres deve ser string ou lista de strings")

# ====================== ESQUEMAS DE VALIDAÇÃO ======================

# Estrutura final dos autores depois de processarmos os CSV.
# A chave é o author_id (int) e o valor é um dicionário com os campos do autor.
authorsSchema = Schema(
    {
        int: {
            'artist_name': non_empty_str,
            'artist_nacionality': non_empty_str,
            'album_title': list,  # lista de títulos de álbuns
            'rights_percentage': And((float), lambda x: 0 <= x <= 100),
            'total_earned': And(float, lambda x: x >= 0),
        }
    }
)

# Estrutura final dos álbuns.
# A chave é o album_id (int) e o valor é um dicionário com os dados do álbum.
albumsSchema = Schema(
    {
        int: {
            'album_title': non_empty_str,
            'artist_name': non_empty_str,
            'album_genere': non_empty_str,
            'album_date': valid_date,
            'unites_sold': non_negative_int,
            'album_price': non_negative_float,
            'tracks': And(list, len),  # lista não vazia de músicas
        }
    }
)

# Estrutura da tabela de administradores.
# Aqui validamos credenciais e garantimos passwords mínimas.
AdminSchema = Schema(
    [
        {
            'admin_id': non_empty_str,
            'username': non_empty_str,
            'password': And(str, lambda p: len(p.strip()) >= 8),
        }
    ]
)

# Estrutura dos dados brutos do raw_tracks.csv.
# Este é o esquema mais importante porque é a base de todo o processamento.
rawSchema = Schema(
    [
        {
            'track_id': positive_int,
            'album_id': positive_int,
            'album_title': non_empty_str,
            'artist_id': positive_int,
            'artist_name': non_empty_str,
            'track_date_recorded': valid_date,
            'track_genres': valid_genres,
            'track_interest': non_negative_int,      # usado como proxy de unidades vendidas
            'track_number': positive_int,
            'track_title': non_empty_str,
            'artist_nacionality': non_empty_str,
            'track_price': positive_float,
        }
    ]
)