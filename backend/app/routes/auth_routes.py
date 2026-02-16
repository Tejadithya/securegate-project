from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas.user_schema import LoginRequest, TokenResponse
from ..auth import create_token

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(username=request.username, password=request.password).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_token(user.id)
        return {"token": token, "username": user.username}
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
