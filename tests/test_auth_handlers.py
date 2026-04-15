import base64
from fastapi.testclient import TestClient
import pytest
from app.main import app


BASE_URL = "http://localhost:8000"
USERNAME = 'admin'
PASSWORD = 'admin'


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    credentials = f"{USERNAME}:{PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {'Authorization': f'Basic {encoded}'}


@pytest.fixture
def wrong_auth():
    credentials = f"wrongusername:wrongpassword"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {'Authorization': f'Basic {encoded}'}


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
    assert "WWW-Authenticate" in response.headers
    assert response.headers['WWW-Authenticate'] == 'Basic'


def test_private_endpoint_wrong_auth(client, wrong_auth):
    response = client.get('/private', headers=wrong_auth)
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
    assert response.headers['WWW-Authenticate'] == 'Basic'


def test_private_endpoint_norm_auth(client, auth_headers):
    response = client.get('/private', headers=auth_headers)
    assert response.status_code == 200


@pytest.mark.parametrize("wrong_headers", [
    {"Authorization": "Basic invalid"},
    {"Authorization": "NotBasic asdf"}
])
def test_private_endpoint_wrong_headers(client, wrong_headers):
    response = client.get('/private', headers=wrong_headers)
    assert response.status_code == 401