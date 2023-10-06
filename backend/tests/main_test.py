from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# TODO: does this need a mock db?

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "\"Service is up\""

def test_topics():
    response = client.get("/topics")
    assert response.status_code == 200

def test_datasets_without_topic():
    response = client.get("/datasets")
    assert response.status_code == 200

def test_datasets_with_topic():
    topic = "sports" # may need to be changed
    response = client.get(f"/datasets?topic={topic}")
    assert response.status_code == 200

def test_dataset():
    uid = "1" # may need to be changed
    response = client.get(f"/dataset/{uid}")
    assert response.status_code == 200
