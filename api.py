from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

CSV_PATH = "shl_catalog.csv"

df = pd.read_csv(CSV_PATH)

# TEXT for embeddings
texts = (df["name"].astype(str) + " - " + df["description"].astype(str)).tolist()

# Load embedding model
model = SentenceTransformer("all-mpnet-base-v2")

print("Encoding dataset...")
emb = model.encode(texts, batch_size=16, show_progress_bar=True)
emb = np.array(emb).astype("float32")

# Normalize for cosine similarity
faiss.normalize_L2(emb)

# Create FAISS index
dimension = emb.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(emb)

app = FastAPI()

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(request: Query):
    q = request.query

    q_emb = model.encode([q])
    q_emb = np.array(q_emb).astype("float32")
    faiss.normalize_L2(q_emb)

    D, I = index.search(q_emb, 10)

    results = []
    for idx in I[0]:
        r = df.iloc[idx]
        results.append({
            "url": str(r["url"]),
            "name": str(r["name"]),
            "description": str(r["description"]),
            "adaptive_support": str(r["adaptive_support"]),
            "remote_support": str(r["remote_support"]),
            "test_type": r["test_type"],
            "duration": int(r["duration"])
        })

    return {"recommended_assessments": results}
