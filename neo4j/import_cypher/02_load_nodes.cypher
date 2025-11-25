// LOAD MOVIES
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row
CREATE (:Movie {movieId: toInteger(row.movieId), title: row.title, rating: toFloat(row.rating), popularity: toFloat(row.popularity), release_date: row.release_date});

// LOAD GENRES
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///genres.csv' AS row
MERGE (:Genre {name: row.genre_name});

// LOAD ACTORS
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///actors.csv' AS row
MERGE (:Actor {name: row.actor_name});

// LOAD DIRECTORS
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///directors.csv' AS row
MERGE (:Director {name: row.person_name});
