from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pydantic import BaseModel

# Secret key for JWT signing (use environment variable in production)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    user_id: int = None

def create_token(user_id: int, expires_delta: timedelta = None):
    """Create a JWT token for the user"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Convert user_id to string for JWT (subject must be a string)
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except JWTError:
        return None
