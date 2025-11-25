# etl/pyspark_etl.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, from_json, trim, udf
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType
import json
import os

spark = SparkSession.builder \
    .appName("TMDB_ETL") \
    .getOrCreate()

# Paths (update if needed)
movies_path = "data/tmdb_5000_movies.csv"
credits_path = "data/tmdb_5000_credits.csv"
out_dir = "data/neo4j_import_csv"
os.makedirs(out_dir, exist_ok=True)

# Read CSVs
movies_df = spark.read.csv(movies_path, header=True, inferSchema=True)
credits_df = spark.read.csv(credits_path, header=True, inferSchema=True)

# Helper to parse json-like strings (genres, cast, crew)
def parse_json_col(df, col_name):
    # assume column contains JSON-like string list: '[{"id":28,"name":"Action"},...]'
    return df.withColumn(col_name, from_json(col(col_name).cast("string"), ArrayType(StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ]))))

movies_df = parse_json_col(movies_df, "genres")
credits_df = parse_json_col(credits_df, "cast")
credits_df = parse_json_col(credits_df, "crew")

# Explode genres into rows
genres_exploded = movies_df.select("id", explode(col("genres")).alias("genre_struct")) \
    .select(col("id").alias("movie_id"), col("genre_struct.id").alias("genre_id"), col("genre_struct.name").alias("genre_name")) \
    .dropDuplicates()

# Movies nodes (select clean columns)
movies_nodes = movies_df.select(
    col("id").alias("movieId"),
    col("title"),
    col("vote_average").alias("rating"),
    col("popularity"),
    col("release_date")
).dropDuplicates()

# Actors (from credits cast)
cast_exploded = credits_df.select(col("movie_id"), explode(col("cast")).alias("cast_struct")) \
    .select(col("movie_id").alias("movieId"),
            col("cast_struct.cast_id").alias("cast_id"),
            col("cast_struct.name").alias("actor_name"),
            col("cast_struct.character").alias("character")) \
    .dropDuplicates()

# Directors from crew (filter job == 'Director')
crew_exploded = credits_df.select(col("movie_id"), explode(col("crew")).alias("crew_struct")) \
    .select(col("movie_id").alias("movieId"),
            col("crew_struct.name").alias("person_name"),
            col("crew_struct.job").alias("job")) \
    .filter(col("job") == "Director") \
    .dropDuplicates()

# Save node CSVs
movies_nodes.toPandas().to_csv(os.path.join(out_dir, "movies.csv"), index=False)
genres_exploded.toPandas().to_csv(os.path.join(out_dir, "genres.csv"), index=False)
cast_exploded.toPandas().to_csv(os.path.join(out_dir, "actors.csv"), index=False)
crew_exploded.toPandas().to_csv(os.path.join(out_dir, "directors.csv"), index=False)

# Create relationship CSVs
# movie-genre
movie_genre = genres_exploded.select(col("movie_id").alias("movieId"), col("genre_name").alias("genreName"))
movie_genre.toPandas().to_csv(os.path.join(out_dir, "movie_genre_rels.csv"), index=False)

# movie-actor
cast_exploded.select("movieId","actor_name","character").toPandas().to_csv(os.path.join(out_dir, "movie_actor_rels.csv"), index=False)

# movie-director
crew_exploded.select("movieId","person_name").toPandas().to_csv(os.path.join(out_dir, "movie_director_rels.csv"), index=False)

print("ETL complete. Neo4j import CSVs in:", out_dir)
