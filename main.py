import psycopg2
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

username = 'postgres'
password = '2711'
database = 'LAB2'
host = 'localhost'
port = '5432'

query_1 = '''
CREATE VIEW Top10DirectorsFilmCount AS
SELECT director.director_name, COUNT(movies.director_id) FROM movies
INNER JOIN director ON director.director_id = movies.director_id
GROUP BY director.director_name
ORDER BY COUNT(movies.director_id) DESC
LIMIT 10
'''

query_2 = '''
CREATE VIEW GenresDistribution AS
SELECT TRIM(genre.genre_name), COUNT(GenreMovies.genre_id) FROM GenreMovies
JOIN genre ON genre.genre_id = GenreMovies.genre_id
GROUP BY genre_name
ORDER BY COUNT(GenreMovies.genre_id) DESC;
'''

query_3 = '''
CREATE VIEW FilmsReleasesPerYear AS
SELECT movies.release_yea, COUNT(movies.movie_id) FROM movies
GROUP BY movies.release_yea
ORDER BY movies.release_yea DESC
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    plt.rcParams.update({'font.size': 5})

    cur = conn.cursor()

# query_1
    cur.execute("DROP VIEW IF EXISTS Top10DirectorsFilmCount")
    cur.execute(query_1)
    cur.execute("SELECT * FROM Top10DirectorsFilmCount")
    country = []
    n_films = []

    for row in cur:
        country.append(row[0])
        n_films.append(row[1])

    x_range = range(len(country))

    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)

    bar_ax.bar(x_range, n_films, label='Total')
    bar_ax.set_title('Топ-10 режисерів за кількістю фільмів у списку')
    bar_ax.set_xlabel('Режисери')
    bar_ax.set_ylabel('Кількість фільмів')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(country, rotation=45)

# query_2
    cur.execute("DROP VIEW IF EXISTS GenresDistribution")
    cur.execute(query_2)
    cur.execute("SELECT * FROM GenresDistribution")
    genres = []
    films = []

    for row in cur:
        genres.append(row[0])
        films.append(row[1])

    pie_ax.pie(films, labels=genres, autopct='%1.1f%%')
    pie_ax.set_title('Частка фільмів за жанром')

# query_3
    cur.execute("DROP VIEW IF EXISTS FilmsReleasesPerYear")
    cur.execute(query_3)
    cur.execute("SELECT * FROM FilmsReleasesPerYear")
    year = []
    count = []

    for row in cur:
        year.append(row[0])
        count.append(row[1])

    x_range = [year[_idx] for _idx in range(len(year)) if _idx % 4 == 0]

    graph_ax.plot(year, count, marker='o', linewidth=0.3, markersize=1)
    graph_ax.set_xlabel('Рік випуску')
    graph_ax.set_ylabel('Кількість фільмів')
    graph_ax.set_title('Кількість випущених фільмів кожного року')
    graph_ax.set_xticks(x_range)
    graph_ax.set_xticklabels(x_range, rotation=90)

    for qnt, price in zip(year, count):
        graph_ax.annotate(price, xy=(qnt, price), xytext=(7, 2), textcoords='offset points')

mng = plt.get_current_fig_manager()
mng.resize(1920, 1080)

plt.subplots_adjust(left=0.1, bottom=0.19, right=0.94, top=0.9, wspace=0.4, hspace=0.4)

plt.savefig("new_graphs.png", format='png', dpi=300)
