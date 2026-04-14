from fastapi.testclient import TestClient
import pytest
from app.main import app


BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200


def test_public_endpoint(client):
    response = client.get('/public')
    assert response.status_code == 200


def test_private_endpoint_no_auth(client):
    response = client.get('/private')
    assert response.status_code == 401
    # assert response.headers