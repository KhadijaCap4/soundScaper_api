from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_music(client, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    music_data = {"title": "Test Music", "artist": "Test Artist", "label": "Test Label", "genre": "Test Genre"}
    response = client.post("/musics", json=music_data, headers=headers)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_music_by_id(client, test_music_id):
    response = client.get(f"/musics/{test_music_id}")
    assert response.status_code == 200
    assert "id" in response.json()

def test_modify_music_title(client, test_music_id, test_user_token, modify_test_music_title):
    # Utiliser la fixture modify_test_music_title
    response = modify_test_music_title
    assert response.status_code == 204

    # Vérifier que le titre a été modifié
    updated_response = client.get(f"/musics/{test_music_id}")
    assert updated_response.status_code == 200
    assert updated_response.json()["title"] == "Modified Music Title"

def test_delete_music(client, test_music_id, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}

    # Vérifier si la musique existe avant la suppression
    initial_response = client.get(f"/musics/{test_music_id}")
    assert initial_response.status_code == 200

    # Supprimer la musique
    delete_response = client.delete(f"/musics/{test_music_id}", headers=headers)
    assert delete_response.status_code == 204

    # Vérifier si la musique est supprimée
    deleted_response = client.get(f"/musics/{test_music_id}")
    assert deleted_response.status_code == 404  # En supposant qu'un statut 404 indique que la musique n'est pas trouvée
