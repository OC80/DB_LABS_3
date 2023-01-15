CREATE TABLE IF NOT EXISTS Movies
(
	Movie_ID INT NOT NULL,    -- PK
	Director_ID INT NOT NULL, -- FK

	Series_title char(255) NOT NULL,
	Release_Yea INT NOT NULL,
	Certificate char(5) NOT NULL,
	Runtime char(10) NOT NULL,
	IMDB_Rating INT NOT NULL,
	Meta_Score INT NOT NULL
);


CREATE TABLE IF NOT EXISTS GenreMovies
(
	Genre_ID INT NOT NULL,
	Movie_ID INT NOT NULL
);


CREATE TABLE IF NOT EXISTS Genre
(
	Genre_ID INT NOT NULL,
	Genre_name char(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Director
(
	Director_ID INT NOT NULL,
	Director_name char(100) NOT NULL
);

-- GENRE
ALTER TABLE Genre ADD PRIMARY KEY(Genre_ID);

-- GENRE - MOVIE
ALTER TABLE GenreMovies ADD PRIMARY KEY(Genre_ID, Movie_ID);

-- MOVIE
ALTER TABLE Movies ADD PRIMARY KEY(Movie_ID);

-- DIRECTOR
ALTER TABLE Director ADD PRIMARY KEY(Director_ID);

-- FK for Genre-Movie table
ALTER TABLE GenreMovies ADD CONSTRAINT FK_GenreMovies_Genre FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID);
ALTER TABLE GenreMovies ADD CONSTRAINT FK_GenreMovies_Movies FOREIGN KEY (Movie_ID) REFERENCES Movies(Movie_ID);

-- FK Movies DirID -> Director DirID
ALTER TABLE Movies ADD CONSTRAINT FK_Movies_Directors FOREIGN KEY (Director_ID) REFERENCES Director(Director_ID);






