import csv
import psycopg2

username = 'postgres'
password = '2711'
database = 'LAB2'
host = 'localhost'
port = '5432'

tables = ["Genre", "Director", "Movies"]


for table in tables:
    connection = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

    cursor = connection.cursor()

    resfile = f"{table.lower()}.csv"

    with open(resfile, "w", newline='', encoding='utf-8') as _f:
        cursor.execute(f"SELECT * FROM {table}")
        _writer = csv.writer(_f)
        _writer.writerow([_item[0] for _item in cursor.description])

        for _row in cursor:
            _writer.writerow([str(_item) for _item in _row])
