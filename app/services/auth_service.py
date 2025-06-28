import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
from app.utils.user_db import users_db

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXPIRATION = int(os.getenv("JWT_EXPIRATION_SECONDS"))

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=EXPIRATION)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload.get("sub"), "role": payload.get("role")}
    except JWTError:
        return None
