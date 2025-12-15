from fastapi.testclient import TestClient
from backend.app.main import app


client = TestClient(app)


def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'


def test_seed_endpoint():
    r = client.get('/seed')
    assert r.status_code == 200
    data = r.json()
    assert 'urls' in data
