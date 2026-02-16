from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
