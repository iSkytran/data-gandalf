from fastapi.testclient import TestClient

def test_health(test_client: TestClient):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.text == "\"Service is up\""

def test_topics(test_client: TestClient):
    response = test_client.get("/topics")
    assert response.status_code == 200

def test_datasets_without_topic(test_client: TestClient):
    response = test_client.get("/datasets")
    assert response.status_code == 200

def test_datasets_with_topic(test_client: TestClient):
    topic = "Topic1" # may need to be changed
    response = test_client.get(f"/datasets?topic={topic}")
    assert response.status_code == 200

def test_dataset(test_client: TestClient):
    uid = "1" # may need to be changed
    response = test_client.get(f"/datasets/{uid}")
    assert response.status_code == 200

