import json
import psycopg2

username = 'postgres'
password = '2711'
database = 'LAB2'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:
    cur = conn.cursor()

    for table in ["Genre", "Director", "Movies", "GenreMovies"]:
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[table] = rows

with open('jsind_dump.json', 'w') as outf:
    json.dump(data, outf, default=str)