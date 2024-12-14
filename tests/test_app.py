# import pytest
# from myapp import app  # Import the Flask app

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# def test_index(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b"Where you are" in response.data

# def test_calculate_distance(client):
#     response = client.post('/calculate_distance', json={'points': [(0, 0), (0, 1), (1, 1)]})
#     assert response.status_code == 200
#     assert 'total_distance' in response.json
#     assert response.json['total_distance'] > 0

import pytest
from myapp import app
import json
from unittest.mock import patch

# Set up the Flask test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the homepage route
def test_homepage(client):
    response = client.get('/homepage')
    assert response.status_code == 200
    assert b'Home - LIBOT' in response.data  # Check if the title is in the response

# Test the index route and get_ip_info
@patch('myapp.requests.get')
def test_index(mock_get, client):
    mock_response = {
        "city": "Test City",
        "region": "Test Region",
        "country": "Test Country",
        "loc": "123.456,-123.456",
        "ip": "192.168.1.1",
        "org": "Test Org",
        "postal": "12345",
        "timezone": "UTC"
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    response = client.get('/')
    assert response.status_code == 200
    assert b'Test City' in response.data  # Check if the city is in the response
    assert b'192.168.1.1' in response.data  # Check if the IP is in the response

# Test the /calculate_distance route
def test_calculate_distance(client):
    data = {
        "points": [
            [0, 0],
            [3, 4]
        ]
    }
    response = client.post('/calculate_distance', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['total_distance'] == 5.0  # The distance between (0, 0) and (3, 4) is 5

