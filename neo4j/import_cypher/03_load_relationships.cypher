// movie -> genre
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///movie_genre_rels.csv' AS row
MATCH (m:Movie {movieId: toInteger(row.movieId)}), (g:Genre {name: row.genreName})
MERGE (m)-[:HAS_GENRE]->(g);

// movie -> actor
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///movie_actor_rels.csv' AS row
MATCH (m:Movie {movieId: toInteger(row.movieId)}), (a:Actor {name: row.actor_name})
MERGE (m)-[:ACTED_BY {character: row.character}]->(a);

// movie -> director
USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///movie_director_rels.csv' AS row
MATCH (m:Movie {movieId: toInteger(row.movieId)}), (d:Director {name: row.person_name})
MERGE (m)-[:DIRECTED_BY]->(d);
