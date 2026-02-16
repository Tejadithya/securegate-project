def test_permission_denied(client, user_token):
    response = client.get(
        "/resource",
        headers={"Authorization": user_token}
    )
    assert response.status_code == 403
