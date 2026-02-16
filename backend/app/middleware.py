from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .database import SessionLocal, get_db
from .models import User
from .auth import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Extract and validate user from JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")

def require_permission(permission_name: str):
    """Dependency to check if user has a specific permission"""
    def checker(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload.get("sub"))
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
        except (JWTError, ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token")

        permissions = {
            p.name
            for role in user.roles
            for p in role.permissions
        }

        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_name}' required"
            )

        return user

    return checker

class AuthorizationMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware to validate JWT tokens for protected routes.
    Routes that start with /resource or /admin require authentication.
    """
    
    PROTECTED_PREFIXES = ["/resource", "/admin"]
    
    async def dispatch(self, request: Request, call_next):
        # Check if route requires authentication
        path = request.url.path
        
        if any(path.startswith(prefix) for prefix in self.PROTECTED_PREFIXES):
            auth_header = request.headers.get("Authorization")
            
            if not auth_header:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Missing authorization header"}
                )
            
            # Extract token
            try:
                scheme, token = auth_header.split()
                if scheme.lower() != "bearer":
                    raise ValueError("Invalid auth scheme")
            except ValueError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authorization header format"}
                )
            
            # Validate token
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = int(payload.get("sub"))
                
                # Store user_id in request state for later use
                request.state.user_id = user_id
            except (JWTError, ValueError):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or expired token"}
                )
        
        response = await call_next(request)
        return response

