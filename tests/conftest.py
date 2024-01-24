import pytest
from fastapi.testclient import TestClient
from main import app
from database.firebase import db

# Fixture pour créer un test client
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

# Fixture pour authentifier un utilisateur de test et retourner le jeton
@pytest.fixture
def test_user_token(client):
    # Supposons des informations d'identification valides pour un utilisateur de test
    credentials = {"username": "test@example.com", "password": "password"}
    response = client.post("/auth/login", data=credentials)
    assert response.status_code == 200
    return response.json()["access_token"]

# Fixture pour ajouter une musique de test et retourner son ID
@pytest.fixture
def test_music_id(client, test_user_token):
    # Supposons une charge utile de musique de test valide
    music_data = {"title": "Test Music", "artist": "Test Artist", "label": "Test Label", "genre": "Test Genre"}
    
    # Authentifier un utilisateur pour obtenir un jeton valide
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Créer la musique de test
    response = client.post("/musics", json=music_data, headers=headers)
    assert response.status_code == 201
    music_id = response.json()["id"]
    
    return music_id

# Fixture pour ajouter un utilisateur de test et retourner son ID
@pytest.fixture
def test_user_id(client, test_user_token):
    # Supposons une charge utile d'utilisateur de test valide
    user_data = {"username": "TestUser", "email": "testuser@example.com", "password": "password"}
    
    # Authentifier un utilisateur pour obtenir un jeton valide
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Créer l'utilisateur de test
    response = client.post("/users", json=user_data, headers=headers)
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    return user_id

# Fixture pour modifier les données d'un utilisateur de test
@pytest.fixture
def modify_test_user(client, test_user_id, test_user_token):
    # Supposons des données d'utilisateur modifiées
    modified_data = {"username": "ModifiedUsername", "email": "modified@example.com", "password": "newpassword"}
    
    # Authentifier un utilisateur pour obtenir un jeton valide
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Modifier les données de l'utilisateur de test
    client.patch(f"/users/{test_user_id}", json=modified_data, headers=headers)

# Fixture pour modifier le titre d'une musique de test
@pytest.fixture
def modify_test_music_title(client, test_music_id, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    modified_data = {"title": "Modified Music Title"}
    
    # Utiliser la méthode PATCH pour modifier la musique
    response = client.patch(f"/musics/{test_music_id}", json=modified_data, headers=headers)
    assert response.status_code == 204
    return response  # Vous pouvez retourner la réponse si nécessaire

# Mettez à jour la fixture delete_test_music pour inclure la création initiale de la musique
@pytest.fixture
def delete_test_music(client, test_user_token):
    # Créer une musique initiale pour les tests de suppression
    headers = {"Authorization": f"Bearer {test_user_token}"}
    music_data = {"title": "Test Music", "artist": "Test Artist", "label": "Test Label", "genre": "Test Genre"}
    response = client.post("/musics", json=music_data, headers=headers)
    assert response.status_code == 201
    music_id = response.json()["id"]

    # Retourner l'ID de la musique pour les tests
    return music_id
