from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..middleware import get_db
from ..models import User
from ..auth import create_token
from ..schemas import LoginRequest, TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=request.username, password=request.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token(user.id)}
