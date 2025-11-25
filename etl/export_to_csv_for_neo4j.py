
import os
import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ExportToNeo4j").getOrCreate()

silver_path = "data/output/clean_movies"
out_dir = "data/neo4j_import_csv"

os.makedirs(out_dir, exist_ok=True)

df = spark.read.parquet(silver_path)

# Extract nodes
movies = df.select("movieId", "title", "rating", "popularity").dropDuplicates()
movies.toPandas().to_csv(os.path.join(out_dir, "movies.csv"), index=False)

genres = df.select("genre_id", "genre_name").dropDuplicates()
genres.toPandas().to_csv(os.path.join(out_dir, "genres.csv"), index=False)

actors = df.select("actor_name").dropDuplicates()
actors.toPandas().to_csv(os.path.join(out_dir, "actors.csv"), index=False)

directors = df.select("director_name").dropDuplicates()
directors.toPandas().to_csv(os.path.join(out_dir, "directors.csv"), index=False)

# Extract relationships
df.select("movieId","genre_name") \
  .dropDuplicates() \
  .toPandas().to_csv(os.path.join(out_dir,"movie_genre_rels.csv"), index=False)

df.select("movieId","actor_name","character") \
  .dropDuplicates() \
  .toPandas().to_csv(os.path.join(out_dir,"movie_actor_rels.csv"), index=False)

df.select("movieId","director_name") \
  .dropDuplicates() \
  .toPandas().to_csv(os.path.join(out_dir,"movie_director_rels.csv"), index=False)

print("Neo4j import CSVs exported to:", out_dir)
