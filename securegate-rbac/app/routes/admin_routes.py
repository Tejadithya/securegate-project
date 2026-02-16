from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..middleware import require_permission, get_db
from ..models import User, Role
from ..schemas import AssignRoleRequest, StatusResponse

router = APIRouter()

@router.post("/assign-role", response_model=StatusResponse)
def assign_role(
    request: AssignRoleRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_permission("ADMIN"))
):
    user = db.query(User).get(request.user_id)
    role = db.query(Role).get(request.role_id)
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    user.roles.append(role)
    db.commit()
    return {"status": "Role assigned"}
