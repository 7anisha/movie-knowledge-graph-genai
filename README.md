# Movie Knowledge Graph & Analytics (Neo4j + PySpark + GenAI)

## Overview
Builds a Movie Knowledge Graph from TMDB datasets, exposes analytics endpoints, and uses an LLM to translate natural language into Cypher for interactive querying.

## Repo structure
(see folder listing)

## Quickstart (local)
1. Put `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` into `data/`.
2. Run ETL:
   - `python etl/pyspark_etl.py`  (requires PySpark)
   - This will create CSVs in `data/neo4j_import_csv/`.
3. Start Neo4j:
   - `cd neo4j && docker compose up -d`
   - Copy CSVs into `neo4j/import/` (or mount them into the import dir)
4. Open Neo4j Browser `http://localhost:7474` (user: neo4j / pass: test).
   - Run `import_cypher/01_constraints.cypher`, then `02_load_nodes.cypher`, then `03_load_relationships.cypher`.
5. Start API:
   - `docker build -f docker/Dockerfile.api -t movie-api .`
   - `docker run -p 8000:8000 --env NEO4J_PASS=test movie-api`
6. Start GenAI (requires OpenAI key):
   - Create `.env` with `OPENAI_API_KEY=...`
   - Use `genai/nl_to_cypher.py` to convert NL → Cypher, then call API `/query`.

## Useful endpoints
- `GET /health`
- `POST /recommend`  { "title": "Inception" }
- `POST /query` { "cypher": "MATCH (m:Movie) RETURN m.title LIMIT 5" }

## Assets
Architecture diagram: `docs/architecture_diagram.png` (sample included: `/mnt/data/90ED87A9-C99F-4B44-B88D-2C657B705C71.jpeg`)
