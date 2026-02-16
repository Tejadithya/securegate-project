from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..middleware import require_permission

router = APIRouter()

@router.get("/")
def get_resource(
    db: Session = Depends(get_db),
    user=Depends(require_permission("READ_DATA"))
):
    """
    Protected route that returns data.
    Only users with READ_DATA permission can access this.
    """
    return {
        "message": "You have access to this resource",
        "user_id": user.id,
        "username": user.username,
        "data": {
            "content": "This is protected resource data",
            "timestamp": "2026-02-15T00:00:00Z"
        }
    }
