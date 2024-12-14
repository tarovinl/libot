import pytest
from myapp import app  # Import the Flask app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Where you are" in response.data

def test_calculate_distance(client):
    response = client.post('/calculate_distance', json={'points': [(0, 0), (0, 1), (1, 1)]})
    assert response.status_code == 200
    assert 'total_distance' in response.json
    assert response.json['total_distance'] > 0
