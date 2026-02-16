import os
import sys

# Set test database URL BEFORE any imports
os.environ['DATABASE_URL'] = "sqlite:///:memory:"

# Also set it before any module caching
if 'app.database' in sys.modules:
    del sys.modules['app.database']
if 'app' in sys.modules:
    del sys.modules['app']

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app.database import get_db
from app.models import User, Role, Permission
from app.auth import create_token

# Create test database
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def user_token(client, db):
    # Create a test user
    user = User(username="testuser", password="testpass")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Login to get token
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    return f"Bearer {response.json()['token']}"
