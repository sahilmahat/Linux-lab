from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_troubleshoot_known_issue():
    response = client.get("/troubleshoot/disk-full")
    assert response.status_code == 200
    data = response.json()
    assert "steps" in data
    assert len(data["steps"]) > 0

def test_troubleshoot_unknown_issue():
    response = client.get("/troubleshoot/unknown-issue")
    assert response.status_code == 200
    data = response.json()
    assert "steps" in data

def test_list_issues():
    response = client.get("/issues")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data

def test_signup():
    response = client.post("/auth/signup", json={
        "username": "testuser",
        "email": "test@linuxlab.com",
        "password": "test1234"
    })
    assert response.status_code in [200, 400]

def test_login_wrong_credentials():
    response = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
