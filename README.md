# 🤖 RoleBot — RAG-Based Internal Chatbot with Role-Based Access Control

Welcome to **RoleBot**, an AI-powered internal chatbot built for the **DS RPC-01 Resume Project Challenge** by [Codebasics](https://github.com/codebasics).

This is a complete implementation of a **RAG-based (Retrieval-Augmented Generation)** chatbot with **role-based access control (RBAC)**, a minimal yet powerful **Streamlit UI**, and integration with OpenAI or Groq LLMs.

---

## 🚀 Features
This chatbot solves FinSolve's data access problem using:
- 🧠 **RAG (Retrieval-Augmented Generation)** via LLaMA 3 (Ollama)
- 🔐 **Role-Based Filtering** at the vector search level
- ⚡ **FastAPI + Streamlit** for interactive chat and login
- 🧾 **Documents** stored per department with metadata
---

## 👥 Role-Based Access Control (RBAC)

| Role               | Permissions                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| C-Level Executives | Full unrestricted access to all documents                                   |
| Finance Team       | Financial reports, expenses, reimbursements                                 |
| Marketing Team     | Campaign performance, customer insights, sales data                         |
| HR Team            | Employee handbook, attendance, leave, payroll                               |
| Engineering Dept.  | System architecture, deployment, CI/CD                                      |
| Employees          | General information (FAQs, company policies, events)                        |

## 🛠 Tech Stack

| Layer         | Tool/Library             |
|---------------|--------------------------|
| Frontend      | Streamlit                |
| Backend       | FastAPI                  |
| Embeddings    | SentenceTransformers     |
| Vector DB     | ChromaDB                 |
| LLM           | LLaMA 3 (via Groq)     |
| Doc Format    | Markdown (.md)           |

---

## 🧪 Sample Users & Roles

| Username | Password     | Role              |
|----------|--------------|-------------------|
| Alice    | ceopass      | c-levelexecutives |
| Bob      | employeepass | employee          |
| Tony     | password123  | engineering       |
| Bruce    | securepass   | marketing         |
| Sam      | financepass  | finance           |
| Natasha  | hrpass123    | hr                |

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
