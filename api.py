from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize FastAPI
app = FastAPI()

# Load vector store
client = chromadb.PersistentClient(path="vector_store")
collection = client.get_collection("shl_assessments")

# Load embedding model
model = SentenceTransformer("all-mpnet-base-v2")

class Query(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(request: Query):
    query = request.query

    # Generate embedding for query
    q_emb = model.encode([query])[0]

    # Retrieve top 10 from Chroma
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=10
    )

    # Format output
    output = []
    for metadata in results["metadatas"][0]:
        output.append({
            "url": metadata["url"],
            "name": metadata["name"],
            "adaptive_support": metadata["adaptive_support"],
            "description": metadata["description"],
            "duration": int(metadata["duration"]),
            "remote_support": metadata["remote_support"],
            "test_type": metadata["test_type"],
        })

    return {"recommended_assessments": output}
