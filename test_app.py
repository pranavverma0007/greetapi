import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_greet_default(client):
    """No name param → defaults to World"""
    response = client.get("/greet")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hey, World!"


def test_greet_with_name(client):
    """Name param is used in the response"""
    response = client.get("/greet?name=Alice")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Hey, Alice!"


def test_greet_returns_json(client):
    """Response Content-Type must be application/json"""
    response = client.get("/greet?name=Bob")
    assert response.content_type == "application/json"


def test_health_check(client):
    """Health endpoint returns status ok"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_greet_custom_prefix(client, monkeypatch):
    """GREETING_PREFIX env var changes the greeting word"""
    monkeypatch.setenv("GREETING_PREFIX", "Hi")
    import importlib
    import app as app_module
    importlib.reload(app_module)
    with app_module.app.test_client() as c:
        response = c.get("/greet?name=Dev")
        data = response.get_json()
        assert data["message"] == "Hi, Dev!"
