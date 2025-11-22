from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import ast

CSV_PATH = "shl_catalog.csv"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"{CSV_PATH} missing")

df = pd.read_csv(CSV_PATH)
if "description" not in df.columns:
    df["description"] = ""

texts = (df["name"].astype(str) + " " + df["description"].astype(str)).tolist()

print("Loading model...")
model = SentenceTransformer(MODEL_NAME)

print("Encoding dataset...")
emb = model.encode(texts, show_progress_bar=True, convert_to_numpy=True).astype("float32")

# Normalize for cosine similarity
emb_norm = emb / np.linalg.norm(emb, axis=1, keepdims=True)

def cosine_top_k(query, k=10):
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    q_emb = q_emb / np.linalg.norm(q_emb)

    # dot product = cosine similarity (because normalized)
    scores = emb_norm @ q_emb.T
    topk_idx = np.argsort(-scores, axis=0)[:k]
    return topk_idx.flatten()

def parse_test_type(v):
    try:
        return ast.literal_eval(v)
    except:
        return [v]

app = FastAPI()

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(request: Query):
    q = request.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty query")

    idxs = cosine_top_k(q, k=10)

    results = []
    for i in idxs:
        row = df.iloc[i]
        results.append({
            "url": row["url"],
            "name": row["name"],
            "adaptive_support": row.get("adaptive_support", "No"),
            "remote_support": row.get("remote_support", "Yes"),
            "description": row.get("description", ""),
            "duration": int(row.get("duration", 0)) if str(row.get("duration", "")).isdigit() else 0,
            "test_type": parse_test_type(row.get("test_type", "['K']"))
        })

    return {"recommended_assessments": results}
