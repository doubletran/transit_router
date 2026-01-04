import pytest
from server import app

@pytest.fixture
def client():
  with app.test_client() as client:
    yield client
def test_get_journey(client):
  response = client.get("/journey")