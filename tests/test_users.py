from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_user(client, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user(client, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    user_data = {"username": "TestUser", "email": "testuser@example.com", "password": "password"}
    response = client.post("/users", json=user_data, headers=headers)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_user_by_id(client, test_user_id, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get(f"/users/{test_user_id}", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

def test_modify_user_title(client, test_user_id, test_user_token, modify_test_user):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    modified_data = {"username": "ModifiedUsername", "email": "modified@example.com", "password": "newpassword"}
    
    response = client.patch(f"/users/{test_user_id}", json=modified_data, headers=headers)
    assert response.status_code == 204

    # Verify that the username has been modified
    updated_response = client.get(f"/users/{test_user_id}", headers=headers)
    assert updated_response.status_code == 200
    assert updated_response.json()["username"] == "ModifiedUsername"

def test_delete_user(client, test_user_id, test_user_token, delete_test_music):
    headers = {"Authorization": f"Bearer {test_user_token}"}

    # Check if the user exists before deletion
    initial_response = client.get(f"/users/{test_user_id}", headers=headers)
    assert initial_response.status_code == 200

    # Delete the user
    delete_response = client.delete(f"/users/{test_user_id}", headers=headers)
    assert delete_response.status_code == 204

    # Check if the user is deleted
    deleted_response = client.get(f"/users/{test_user_id}", headers=headers)
    assert deleted_response.status_code == 404  # Assuming a 404 status indicates the user is not found
