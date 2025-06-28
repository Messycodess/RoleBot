from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle
import pandas as pd

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_DIR = "vector_data"
RESOURCE_DIR = "resources/data"


def load_documents(role: str) -> list[str]:
    role_path = os.path.join(RESOURCE_DIR, role)
    documents = []

    if not os.path.exists(role_path):
        print(f"⚠️ Directory for role '{role}' does not exist: {role_path}")
        return []

    for filename in os.listdir(role_path):
        file_path = os.path.join(role_path, filename)

        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(file_path)
                for col in df.select_dtypes(include=[object]):
                    documents.extend(df[col].dropna().astype(str).tolist())

            elif filename.endswith(".txt") or filename.endswith(".md"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    if text:
                        documents.append(text)

        except Exception as e:
            print(f"⚠️ Failed to read {file_path}: {e}")

    print(f"✅ Loaded {len(documents)} documents for role: {role}")
    return documents


def build_faiss_index(role: str, documents: list[str]):
    if not documents:
        print(f"⚠️ Skipping {role}, no documents found.")
        return

    vectors = embedding_model.encode(documents, show_progress_bar=True)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    os.makedirs(VECTOR_DIR, exist_ok=True)
    faiss.write_index(index, f"{VECTOR_DIR}/{role}_index.faiss")

    with open(f"{VECTOR_DIR}/{role}_docs.pkl", "wb") as f:
        pickle.dump(documents, f)

    print(f"✅ FAISS index built and saved for role: {role}")


if __name__ == "__main__":
    roles = ["general", "marketing", "engineering", "finance", "hr"]
    for role in roles:
        docs = load_documents(role)
        build_faiss_index(role, docs)
