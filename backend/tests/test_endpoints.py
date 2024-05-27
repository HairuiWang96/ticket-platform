# backend/tests/test_endpoints.py
import logging
from fastapi.testclient import TestClient
from backend.main import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TestClient(app)


# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}


def test_list_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    # Assert that the response contains a list of tickets
    assert isinstance(response.json(), list)


def test_read_ticket():
    # Assuming ticket ID 1 exists
    response = client.get("/tickets/1/")
    logger.info(f"GET /tickets/1/ response: {response.status_code}, {response.json()}")
    assert response.status_code == 200
    # Assert that the response contains ticket details
    assert "id" in response.json()
    assert "status" in response.json()
    assert "priority" in response.json()
    # assert "assignee" in response.json()


def test_update_ticket():
    # Assuming ticket ID 1 exists
    response = client.put("/tickets/1/", json={"subject": "Issue with login", "status": "Open", "assignee": "Bob", "priority": "Low"})
    logger.info(f"PUT /tickets/1/ response: {response.status_code}, {response.json()}")
    assert response.status_code == 200
    # Assert that the response contains updated ticket details
    assert "id" in response.json()
    assert "status" in response.json()
    assert response.json()["status"] == "Open"
    assert "priority" in response.json()
    assert response.json()["priority"] == "Low"
    assert "assignee" in response.json()
    assert response.json()["assignee"] == "Bob"

