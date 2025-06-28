from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user, create_access_token, decode_access_token
from app.schemas.token import Token
from fastapi import Request
from app.services.retriever_service import retrieve_similar_docs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

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

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = auth_header.split(" ")[1]
    user_data = decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_data

@app.post("/chat")
def chat(query: str, user=Depends(get_current_user)):
    if user["role"] not in ["engineering", "hr", "finance", "marketing"]:
        raise HTTPException(status_code=403, detail="Access denied for your role.")
    
    # Dummy role-based logic for now
    return {
        "response": f"Hi {user['username']}, you asked: '{query}' (role: {user['role']})"
    }


@app.get("/test-retrieve")
def test_retrieve(query: str, request: Request):
    user = get_current_user(request)
    return retrieve_similar_docs(query, user["role"])
