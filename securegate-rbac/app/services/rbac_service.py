from ..repositories.user_repo import UserRepository
from ..repositories.role_repo import RoleRepository

class RBACService:
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.user_repo = user_repo
        self.role_repo = role_repo

    def assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        user = self.user_repo.get_user_by_id(user_id)
        role = self.role_repo.get_role_by_id(role_id)
        if user and role:
            user.roles.append(role)
            return True
        return False

    def check_permission(self, user_id: int, permission_name: str) -> bool:
        user = self.user_repo.get_user_by_id(user_id)
        if user:
            permissions = {p.name for role in user.roles for p in role.permissions}
            return permission_name in permissions
        return False
