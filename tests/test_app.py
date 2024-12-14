import pytest
import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from myapp import app



# Create a fixture to set up the Flask app for testing
@pytest.fixture
def client():

    with app.test_client() as client:
        yield client

# Test the index route
def test_index(client):
    print("Testing index...")
    # Send a GET request to the '/' route
    print("Sending GET request to the '/' route...")
    response = client.get('/')

    # Check that the status code is 200 (OK)
    print("Check that the status code is 200 (OK)...")
    assert response.status_code == 200
    
    # Check if the response contains specific content
    print("Check if the response contains specific content...")
    assert b'Where you are' in response.data
    assert b'Check your coordinates' in response.data
    print("Index test DONE...")
# Test the calculate_distance route
def test_calculate_distance(client):
    # Send a POST request with sample data to '/calculate_distance'
    json_data = {
        'points': [(0, 0), (0, 1), (1, 1)]  # Example coordinates
    }
    response = client.post('/calculate_distance', json=json_data)
    
    # Check that the status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the total_distance key is in the response data
    assert 'total_distance' in response.json
    assert response.json['total_distance'] > 0

# Test the homepage route
def test_homepage(client):
    # Send a GET request to the '/homepage' route
    response = client.get('/homepage')
    
    # Check that the status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the response contains the title 'Home - LIBOT'
    assert b'<title>Home - LIBOT</title>' in response.data
