DO $$
    DECLARE
     genre_idx Genre.genre_id%TYPE;
     genre_name Genre.genre_name%TYPE;

    BEGIN
     genre_idx := 'A';
     genre_name := 'B';
     FOR counter IN 1..20
         LOOP
            INSERT INTO Genre (genre_id, genre_name)
            	VALUES (CONCAT(SUBSTRING(genre_idx, 1, 2), counter * 5), CONCAT(SUBSTRING(genre_name, 1, 2), counter * 3));
         END LOOP;
    END;
    $$