import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from database.firebase import db

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="function")
def todo_id():
    todo_data = {"Title": "Test Todo", "Description": "Test Description", "Completed": False}
    todo_ref = db.child("Task").push(todo_data)
    todo_id = todo_ref["name"]
    yield todo_id
    db.child("Task").child(todo_id).remove()

def test_get_todo_by_id(test_app, todo_id):
    response = test_app.get(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == todo_id
    
def test_get_non_existing_todo_by_id(test_app):
    todo_id = "f15397f8-9b49-4da7-871d-a04c7969e2dc"  
    response = test_app.get(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_todo(test_app, todo_id):
    response = test_app.patch(
        f"/todos/{todo_id}",
        json={"Title": "Updated Title", "Description": "Updated Description", "Completed": False}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["Title"] == "Updated Title"

def test_delete_todo(test_app, todo_id):
    response = test_app.delete(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_non_existing_todo(test_app):
    todo_id = "f15397f8-7b49-4da7-871d-a04c7969e2dc"  
    response = test_app.delete(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND