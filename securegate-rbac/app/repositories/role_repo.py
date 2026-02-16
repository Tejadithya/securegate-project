from sqlalchemy.orm import Session
from ..models import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, role_id: int) -> Role:
        return self.db.query(Role).get(role_id)

    def get_role_by_name(self, name: str) -> Role:
        return self.db.query(Role).filter_by(name=name).first()
