"""Authentication routes for EnQue API.
Implements user registration, login (JWT) and a "me" endpoint.
Uses BCrypt for password hashing (passlib) and python‑jose for JWT handling.
All routes are protected with the `get_current_user` dependency where appropriate.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import User
from backend.app.utils.security import hash_password, verify_password
from backend.app.utils.jwt import create_access_token, verify_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    # Hash password and create user
    hashed = hash_password(req.password)
    user = User(name=req.name, email=req.email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    # Issue JWT
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}

from backend.app.utils.auth_deps import get_current_user

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email}

