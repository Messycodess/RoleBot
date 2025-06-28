import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

VECTOR_DIR = "vector_data"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_faiss_index(role: str):
    index_path = os.path.join(VECTOR_DIR, f"{role}_index.faiss")
    docs_path = os.path.join(VECTOR_DIR, f"{role}_docs.pkl")

    if not os.path.exists(index_path) or not os.path.exists(docs_path):
        raise ValueError(f"No vector index found for role: {role}")

    index = faiss.read_index(index_path)
    with open(docs_path, "rb") as f:
        documents = pickle.load(f)

    return index, documents


def retrieve_similar_docs(query: str, role: str, top_k: int = 3) -> list[str]:
    index, documents = load_faiss_index(role)
    query_vector = embedding_model.encode([query])
    
    distances, indices = index.search(query_vector, top_k)
    results = [documents[i] for i in indices[0] if i < len(documents)]
    
    return results
