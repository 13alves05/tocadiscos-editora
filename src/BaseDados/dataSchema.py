from schema import Schema, And, Use, Or
import re

# Helper validators
def non_empty_str(value):
    if not value or not str(value).strip():
        raise ValueError("Must be a non-empty string")
    return str(value).strip()

def positive_int(value):
    i = int(value)
    if i <= 0:
        raise ValueError(f"{value} must be a positive integer")
    return i

def non_negative_int(value):
    i = int(value)
    if i < 0:
        raise ValueError(f"{value} must be non-negative")
    return i

def positive_float(value):
    f = float(value)
    if f <= 0:
        raise ValueError(f"{value} must be positive")
    return f

def non_negative_float(value):
    f = float(value)
    if f < 0:
        raise ValueError(f"{value} must be non-negative")
    return f

def valid_date(value):
    s = str(value)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        raise ValueError(f"{s} is not a valid YYYY-MM-DD date")
    return s

# -------------------------------------------------
# Schema for the processed authors structure (not raw input)
# -------------------------------------------------
authorsSchema = Schema(
    {
        int: {  # key = artist_id (int)
            'artist_name': And(str, len),
            'artist_nacionality': And(str, len),
            'album_title': And(list, len),  # list of (album_id:int, album_title:str) tuples
            'rights_percentage': And(Use(int), lambda x: 10 <= x <= 50),
            'total_earned': And(Use(float), lambda x: x >= 0),
        }
    }
)

# -------------------------------------------------
# Schema for the processed albums structure
# -------------------------------------------------
albumsSchema = Schema(
    {
        int: {  # key = album_id (int)
            'album_title': And(str, len),
            'artist_name': And(str, len),
            'album_genere': And(str, len),
            'album_date': And(str, valid_date),
            'unites_sold': And(Use(int), lambda x: x >= 0),
            'album_price': And(Use(float), lambda x: x >= 0),
            'tracks': And(list, len),  # list of (track_id:int, track_title:str) tuples
        }
    }
)

# -------------------------------------------------
# Admin schema (unchanged, just safer)
# -------------------------------------------------
AdminSchema = Schema(
    [
        {
            'admin_id': And(str, len),
            'username': And(str, len),
            'password': And(str, lambda p: len(p) >= 8),
        }
    ]
)

# -------------------------------------------------
# Raw input schema - this is the most important one
# because your feed/update functions read from "line"
# -------------------------------------------------
rawSchema = Schema(
    [
        {
            'track_id': And(Use(int), positive_int),
            'album_id': And(Use(int), positive_int),
            'album_title': And(non_empty_str),
            'artist_id': And(Use(int), positive_int),
            'artist_name': And(non_empty_str),
            'track_date_recorded': And(valid_date),
            'track_genres': And(Or(str, list), len),  # can be "Rock" or ["Rock", "Pop"]
            'track_interest': And(Use(int), non_negative_int),  # used as "units sold" proxy
            'track_number': And(Use(int), positive_int),
            'track_title': And(non_empty_str),
            'artist_nacionality': And(non_empty_str),
            'track_price': And(Use(float), positive_float),
        }
    ]
)