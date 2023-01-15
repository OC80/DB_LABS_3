import random
from csv import DictReader
from typing import List, Tuple

import psycopg2

username = 'postgres'
password = '2711'
database = 'LAB2'
host = 'localhost'
port = '5432'

file = "imdb_top_1000.csv"


def get_genre_and_dir_tables() -> Tuple[dict, dict]:
    with open(file, "r") as inf:
        dr = DictReader(inf)

        _genres = {}
        _initials = {}

        _d_id = 0
        _g_id = 0

        for val in dr:
            _name = val['Director'].replace("'", "`")

            if _name not in _initials.values():
                _initials[_d_id] = _name
                _d_id += 1

            for _genre in val['Genre'].split(", "):
                if _genre not in _genres.values():
                    _genres[_g_id] = _genre
                    _g_id += 1

        return _genres, _initials


def execute_import():
    _query = get_query()
    print(_query)

    _connection = psycopg2.connect(user=username, password=password, dbname=database,
                                   host=host, port=port)

    _res = []

    with _connection:
        _cursor = _connection.cursor()
        _cursor.execute(_query)


def get_query() -> str:
    _main_table = {}
    _genres, _directors = get_genre_and_dir_tables()

    _res = "DELETE FROM GenreMovies;\nDELETE FROM Movies;\nDELETE FROM Director;\n DELETE FROM Genre;\n\n"

    for _d_id, _name in _directors.items():
        _res += f"INSERT INTO Director (director_id, director_name)\n" \
                f"\tVALUES('{_d_id}', '{_name}');\n"

    _res += "\n\n"

    for _id_genre, _genre in _genres.items():
        _res += f"INSERT INTO Genre (genre_id, genre_name)\n" \
                f"\tVALUES('{_id_genre}', '{_genre}');\n"

    _res += "\n\n"

    _m_id = 0
    with open(file, "r") as inf:
        dr = DictReader(inf)
        for val in dr:
            for _id, _name in _directors.items():
                if _name == val['Director'].replace("'", "`"):
                    _dir_id = _id

            _delimit = "'"
            _res += f"INSERT INTO Movies (movie_id, series_title, release_yea, certificate, runtime, imdb_rating, meta_score, director_id)\n " \
                    f"\tVALUES('{_m_id}', '{val['Series_Title'].replace(f'{_delimit}', '`')}', '{val['Released_Year']}', '{val['Certificate'][0:5]}', '{val['Runtime']}', '{int(float(val['IMDB_Rating']) * 10)}', '{val['Meta_score'] if val['Meta_score'] != '' else -1}', '{_dir_id}');\n"
            _m_id += 1

    _m_id = 0
    with open(file, "r") as inf:
        dr = DictReader(inf)
        for val in dr:
            for _genre in val['Genre'].split(", "):
                _g_id = 0
                for _id, _g in _genres.items():
                    if _g == _genre:
                        _g_id = _id

                _res += f"INSERT INTO GenreMovies (movie_id, genre_id)\n " \
                        f"\tVALUES('{_m_id}', '{_g_id}');\n"
            _m_id += 1

    return _res


execute_import()
