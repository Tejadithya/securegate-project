from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str

class AssignRoleRequest(BaseModel):
    user_id: int
    role_id: int

class AssignRoleResponse(BaseModel):
    status: str
