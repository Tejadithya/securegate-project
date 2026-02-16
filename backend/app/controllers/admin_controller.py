from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..middleware import require_permission, get_db
from ..models import User, Role
from ..schemas import AssignRoleRequest, AssignRoleResponse

router = APIRouter()

@router.post("/assign-role", response_model=AssignRoleResponse)
def assign_role(
    request: AssignRoleRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_permission("ADMIN"))
):
    user = db.query(User).get(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role = db.query(Role).get(request.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
    return {"status": "Role assigned"}
