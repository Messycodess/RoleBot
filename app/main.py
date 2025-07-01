from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from app.services.auth_service import authenticate_user, create_access_token, decode_access_token
from app.services.retriever_service import retrieve_similar_docs, generate_rag_response
from app.schemas.token import Token
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# OAuth2 scheme for Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ✅ Pydantic model for /chat request
class ChatRequest(BaseModel):
    query: str


# === /login ===
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })
    return {"access_token": token, "token_type": "bearer"}


# === Get current user from token ===
def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_data


# ✅ === /chat endpoint ==
@app.post("/chat")
def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    query = request.query
    role = current_user["role"]  # ✅ fixed here
    username = current_user["username"]

    if role not in ["engineering", "hr", "finance", "marketing", "general"]:
        raise HTTPException(status_code=403, detail="Access denied for your role")

    relevant_docs = retrieve_similar_docs(query, role)
    response = generate_rag_response(query, relevant_docs)

    return {
        "username": username,
        "role": role,
        "query": query,
        "answer": response
    }



# === /test-retrieve endpoint ===
@app.get("/test-retrieve")
def test_retrieve(query: str, current_user: dict = Depends(get_current_user)):
    return retrieve_similar_docs(query, current_user["role"])

#uvicorn main:app --reload