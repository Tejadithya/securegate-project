from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .database import SessionLocal, get_db
from .models import User
from .auth import SECRET_KEY, ALGORITHM

bearer = HTTPBearer()

def require_permission(permission_name: str):
    def checker(credentials = Depends(bearer), db: Session = Depends(get_db)):
        try:
            token = credentials.credentials if credentials else None
            if not token:
                raise HTTPException(status_code=401, detail="Invalid token")
                
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload.get("sub"))
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=401, detail="Invalid token")
                
        except (JWTError, ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token")
        except HTTPException:
            raise

        permissions = {
            p.name
            for role in user.roles
            for p in role.permissions
        }

        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return user

    return checker
