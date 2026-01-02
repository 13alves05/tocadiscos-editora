"""
Esquemas de validação usando a biblioteca "schema"
Criámos isto para validar os dados que vêm dos CSV e das estruturas internas.
O objetivo é evitar que dados mal formatados entrem no sistema.
Tivemos problemas com o type checker (Pylance/mypy) quando usávamos And(Or(), len)
e And(Use(), lambda) diretamente - ele não conseguia inferir os tipos.
A solução mais simples e que funciona sempre é usar funções auxiliares que já fazem
a conversão e a validação juntas. Assim o código fica limpo e o type checker cala-se.
"""

from schema import Schema, And
import re

# ====================== FUNÇÕES AUXILIARES DE VALIDAÇÃO ======================

def non_empty_str(value):
    # Garante que é uma string não vazia
    if not value or not str(value).strip():
        raise ValueError("Tem de ser uma string não vazia")
    return str(value).strip()

def positive_int(value):
    # Converte para inteiro e verifica se é positivo (> 0)
    try:
        i = int(value)
        if i <= 0:
            raise ValueError
        return i
    except:
        raise ValueError(f"{value} tem de ser um inteiro positivo")

def non_negative_int(value):
    # Converte para inteiro e verifica se é não negativo (>= 0)
    try:
        i = int(value)
        if i < 0:
            raise ValueError
        return i
    except:
        raise ValueError(f"{value} tem de ser um inteiro não negativo")

def positive_float(value):
    # Converte para float e verifica se é positivo (> 0)
    try:
        f = float(value)
        if f <= 0:
            raise ValueError
        return f
    except:
        raise ValueError(f"{value} tem de ser um número positivo")

def non_negative_float(value):
    # Converte para float e verifica se é não negativo (>= 0)
    try:
        f = float(value)
        if f < 0:
            raise ValueError
        return f
    except:
        raise ValueError(f"{value} tem de ser um número não negativo")

def valid_date(value):
    # Verifica se a data está no formato YYYY-MM-DD
    s = str(value)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        raise ValueError(f"{s} não é uma data válida (deve ser YYYY-MM-DD)")
    return s

def valid_genres(value):
    # Aceita string não vazia ou lista de strings não vazias para track_genres
    if isinstance(value, str):
        if value.strip():
            return value.strip()
        raise ValueError("Género musical não pode ser vazio")
    elif isinstance(value, list):
        if len(value) > 0 and all(isinstance(g, str) and g.strip() for g in value):
            return [g.strip() for g in value]
        raise ValueError("Lista de géneros inválida ou vazia")
    else:
        raise ValueError("track_genres deve ser string ou lista de strings")

# ====================== ESQUEMAS DE VALIDAÇÃO ======================

# Estrutura processada dos autores (dicionário com author_id como chave)
authorsSchema = Schema(
    {
        int: {
            'artist_name': non_empty_str,
            'artist_nacionality': non_empty_str,
            'album_title': And(list, len),  # lista não vazia de álbuns
            'rights_percentage': And(positive_int, lambda x: 10 <= x <= 50),
            'total_earned': non_negative_float,
        }
    }
)

# Estrutura processada dos álbuns (dicionário com album_id como chave)
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

# Tabela de administradores
AdminSchema = Schema(
    [
        {
            'admin_id': non_empty_str,
            'username': non_empty_str,
            'password': And(str, lambda p: len(p.strip()) >= 8),
        }
    ]
)

# Dados brutos do raw_tracks.csv – o mais importante para o processamento inicial
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