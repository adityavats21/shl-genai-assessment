import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
import os
import ast

# Load CSV data
df = pd.read_csv("shl_catalog.csv")

# Convert test_type string → list if needed
def parse_list(x):
    try:
        return ast.literal_eval(x)
    except:
        return [x]

df["test_type"] = df["test_type"].apply(parse_list)

# Create text field for embeddings
df["text_for_embedding"] = df["name"] + " - " + df["description"]

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(df["text_for_embedding"].tolist(), show_progress_bar=True)

# Initialize ChromaDB
persist_dir = "vector_store"
os.makedirs(persist_dir, exist_ok=True)

client = chromadb.PersistentClient(path=persist_dir)

# Create collection
collection = client.get_or_create_collection(
    name="shl_assessments",
    metadata={"hnsw:space": "cosine"}
)

# Clear existing records
existing = collection.count()
if existing > 0:
    print(f"Removing {existing} existing entries...")
    collection.delete(ids=[str(i) for i in range(existing)])

print("Adding embeddings to ChromaDB...")

for idx, row in df.iterrows():
    metadata = {
        "url": row["url"],
        "name": row["name"],
        "description": row["description"],
        "adaptive_support": row["adaptive_support"],
        "remote_support": row["remote_support"],
        "test_type": row["test_type"],
        "duration": int(row["duration"]) if not pd.isna(row["duration"]) else 0
    }

    collection.add(
        ids=[str(idx)],
        documents=[row["text_for_embedding"]],
        metadatas=[metadata],
        embeddings=[embeddings[idx]]
    )

print("Vector store created successfully!")
print("You can now run the API to perform recommendations.")
