from sqlalchemy.orm import Session
from ..models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter_by(username=username).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).get(user_id)
