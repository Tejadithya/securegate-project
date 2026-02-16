import pytest
from app.models import User, Role, Permission

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

def test_permission_denied(client, user_token):
    response = client.post(
        "/admin/assign-role",
        json={"user_id": 1, "role_id": 1},
        headers={"Authorization": user_token}
    )
    assert response.status_code == 403
