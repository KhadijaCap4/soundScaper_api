from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test authentification endpoints
def test_signup(client):
    response = client.post("/auth/signup", json={"email": "test5@example.com", "password": "password"})
    assert response.status_code == 201
    assert "Nouvel utilisateur créé avec id" in response.json()["message"]

def test_login(client):
    credentials = {"username": "test@example.com", "password": "password"}
    response = client.post("/auth/login", data=credentials)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_me(client, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert "uid" in response.json()