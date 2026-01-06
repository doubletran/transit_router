import pytest
from server import app

@pytest.fixture
def client():
  with app.test_client() as client:
    yield client
def test_getJourney(client):
  response = client.get("/journey", query_string=
                        {"fromlat": 36.93572, 
                         "fromlon":-121.77362,
                         "tolat": 37.75787,
                         "tolon": -122.479853})
  print("RESPONSE")
  print(response.text)
  
  
  
  