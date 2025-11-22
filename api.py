from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import threading

app = FastAPI(title="SHL Assessment Recommender")

CSV_PATH = "shl_catalog.csv"

df = pd.read_csv(CSV_PATH)
df["description"] = df["description"].fillna("")

texts = (df["name"].astype(str) + " - " + df["description"].astype(str)).tolist()

model = None
model_lock = threading.Lock()
embeddings = None

def load_model_once():
    global model, embeddings
    with model_lock:
        if model is None:
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            embeddings = model.encode(texts, convert_to_numpy=True)

@app.get("/health")
def health():
    return {"status": "healthy"}

class Query(BaseModel):
    query: str

@app.post("/recommend")
def recommend(q: Query):
    if not q.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")

    # load at first request only
    load_model_once()

    q_emb = model.encode([q.query], convert_to_numpy=True)

    sims = cosine_similarity(q_emb, embeddings)[0]
    top_idx = sims.argsort()[::-1][:10]

    results = []
    for idx in top_idx:
        row = df.iloc[idx]
        results.append({
            "url": row["url"],
            "name": row["name"],
            "description": row["description"],
        })

    return {"recommended_assessments": results}
