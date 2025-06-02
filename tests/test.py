from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_recommend_endpoint():
    r = client.get("/recommend?q=dream")
    assert r.status_code == 200
    body = r.json()
    assert body["variant"] in ("A", "B")
    assert len(body["results"]) >= 3