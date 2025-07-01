# 🤖 RoleBot — RAG-Based Internal Chatbot with Role-Based Access Control

Welcome to **RoleBot**, an AI-powered internal chatbot built for the **DS RPC-01 Resume Project Challenge** by [Codebasics](https://github.com/codebasics).

This is a complete implementation of a **RAG-based (Retrieval-Augmented Generation)** chatbot with **role-based access control (RBAC)**, a minimal yet powerful **Streamlit UI**, and integration with OpenAI or Groq LLMs.

---

## 🚀 Features

### ✅ 1. Role-Based Access Control (RBAC)
- Secure login using **JWT authentication**
- Role-aware responses for HR, Finance, Marketing, Engineering, Executives, and Employees
- Each role sees tailored answers from internal documents

### 🧠 2. Retrieval-Augmented Generation (RAG)
- Documents stored in `.txt` format per department
- Uses **FAISS** for vector similarity search
- Embeddings generated using OpenAI's `text-embedding-3-small` model

### 🌐 3. Streamlit Frontend
- Clean, responsive UI for chat interaction
- Easy to use for non-technical users
- Real-time LLM answers streamed to the user

### ⚡ 4. LLM Integration
- Supports **OpenAI GPT-3.5** or **Groq (Mixtral/LLama3)** for blazing fast responses
- Modular logic to swap models or providers easily

---

## 🗂️ Project Structure

RoleBot/
├── app/
│ ├── main.py # FastAPI backend with auth & routing
│ ├── services/
│ │ └── retriever_service.py # Embedding & vector search logic
│ └── schemas/
│ └── chat.py # Pydantic schemas
├── resources/ # Source text files (HR.txt, Finance.txt, etc.)
├── vector_data/ # FAISS index files stored here
├── streamlit_ui.py # Frontend chat UI
├── .env.example # Environment variable template
├── pyproject.toml # Project dependencies
├── README.md

---


## 🛠️ Setup Instructions

### 1. Clone the Repo (Forked from Codebasics)
```bash
git clone https://github.com/Messycodess/RoleBot.git
cd RoleBot
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Activate the environment
# On Unix or MacOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file (or rename `.env.example`) and add the following:

```env
GROQ_API_KEY=your-groq-api-key
JWT_SECRET_KEY=your-jwt-secret
```

> 🔁 If you're using OpenRouter or OpenAI instead of Groq, adjust the key name accordingly.

### 4. Start the FastAPI Backend
```bash
uvicorn app.main:app --reload
```

### 5. Run the Streamlit Frontend
```bash
streamlit run streamlit_ui.py
```
