from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    payload ={"username": "testuser", "password": "testpass","email": "test@gmail.com","phone": "1234567890","role":"student"}
    response = client.post("/auth/register", json=payload)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["message"] == "User registered"

def test_login():
    pass
