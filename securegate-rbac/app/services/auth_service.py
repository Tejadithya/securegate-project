from ..repositories.user_repo import UserRepository
from ..auth import create_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, username: str, password: str) -> str:
        user = self.user_repo.get_user_by_username(username)
        if user and user.password == password:  # In production, hash passwords
            return create_token(user.id)
        return None
