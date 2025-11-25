# api/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "test")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
app = FastAPI(title="Movie KG API")

class NLQuery(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/query")
def run_cypher(cypher: dict):
    q = cypher.get("cypher")
    if not q:
        raise HTTPException(status_code=400, detail="No cypher query provided")
    with driver.session() as session:
        res = session.run(q)
        return {"data": [r.data() for r in res]}

@app.post("/recommend")
def recommend_by_title(payload: dict):
    title = payload.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="title required")
    q = """
    MATCH (m:Movie {title:$title})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie)
    WHERE rec.title <> $title
    RETURN rec.title AS title, rec.rating AS rating, collect(g.name) AS shared_genres
    ORDER BY rec.rating DESC, rec.popularity DESC
    LIMIT 10
    """
    with driver.session() as session:
        res = session.run(q, title=title)
        return {"recommendations":[r.data() for r in res]}

# for quick interactive testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
