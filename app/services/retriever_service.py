import os
import pickle
from typing import List
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load embedding model (same used for vector generation)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Directory where FAISS index + docs are stored
VECTOR_DIR = "vector_data"


def load_faiss_index(role: str):
    """
    Load FAISS index and corresponding documents for a given role.
    """
    index_path = os.path.join(VECTOR_DIR, f"{role}_index.faiss")
    docs_path = os.path.join(VECTOR_DIR, f"{role}_docs.pkl")

    if not os.path.exists(index_path) or not os.path.exists(docs_path):
        raise ValueError(f"Vector data for role '{role}' not found.")

    # Load FAISS index
    index = faiss.read_index(index_path)

    # Load associated documents
    with open(docs_path, "rb") as f:
        documents = pickle.load(f)

    return index, documents


def retrieve_similar_docs(query: str, role: str, top_k: int = 3) -> List[str]:
    """
    Embed the query and search top_k most similar documents using FAISS index.
    """
    index, documents = load_faiss_index(role)

    # Encode query to vector
    query_vec = embedding_model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    # Search for top_k similar docs
    scores, indices = index.search(query_vec, top_k)
    retrieved = [documents[i] for i in indices[0] if i < len(documents)]

    return retrieved


def generate_rag_response(query: str, context_docs: List[str]) -> str:
    import os
    from openai import OpenAI

    print("🔍 [Debug] Starting RAG response generation...")

    api_key = os.getenv("OPENROUTER_KEY")
    if not api_key:
        print("❌ [Debug] OPENROUTER_KEY not found in environment.")
        return "❌ OPENROUTER_KEY not set in .env"

    print("✅ [Debug] API key loaded.")

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        print("✅ [Debug] OpenAI client initialized.")

        context = "\n\n".join(context_docs)
        prompt = f"""You are an intelligent assistant specialized in the domain of the user asking the question.

Context:
{context}

User Question:
{query}

Answer:"""

        print("📤 [Debug] Sending request to OpenRouter...")
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful and polite company assistant. Summarize and answer the user's query based only on the context below.Respond in simple, human-like language. Be clear and friendly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        print("✅ [Debug] Got response.")
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ [Debug] Exception occurred:", e)
        return "❌ Failed to generate a response. See terminal logs."
#what is guidelined for github workflow