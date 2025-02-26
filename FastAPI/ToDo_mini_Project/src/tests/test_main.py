from fastapi.testclient import TestClient # for test

from main import app

client = TestClient(app=app) # sending API

def test_health_check():
    response = client.get("/") # ping: pong
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}

def test_get_todos():
    # order=ASC
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": True},
            {"id": 3, "contents": "FastAPI Section 2", "is_done": False},
        ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 3, "contents": "FastAPI Section 2", "is_done": False},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": True},
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
        ]
    }