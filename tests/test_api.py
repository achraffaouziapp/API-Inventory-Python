import sys
from pathlib import Path

import pytest

# Ajouter la racine du projet au PYTHONPATH pour GitHub Actions
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.main import app


@pytest.fixture()
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_health_returns_200(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "OK"
    assert data["version"] == "1.0"


def test_servers_returns_list(client):
    res = client.get("/api/v1/servers")
    assert res.status_code == 200
    data = res.get_json()
    assert "servers" in data
    assert "count" in data
    assert isinstance(data["servers"], list)
    assert data["count"] == 2


def test_server_by_id_valid(client):
    res = client.get("/api/v1/servers/1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == 1
    assert data["hostname"] == "web-prod-01"
    assert data["ip"] == "10.0.0.1"
    assert data["status"] == "up"


def test_server_by_id_invalid_returns_404(client):
    res = client.get("/api/v1/servers/999")
    assert res.status_code == 404
    data = res.get_json()
    assert data == {"error": "Server not found"}
