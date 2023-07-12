import pytest
from app import app,weather_data
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_weather_valid_city(client):
    response = client.get("/weather/San Francisco")
    assert response.status_code == 200
    data = response.get_json()  # Access response data as JSON
    assert "temperature" in data
    assert "weather" in data

def test_add_weather_valid_data(client):
    data = {"city": "Chicago"}
    response = client.post("/weather", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert b"Missing required fields in the request data." in response.data


def test_add_weather_invalid_data(client):
    data = {
        "city": "Denver",
        "weather": "Sunny"
    }
    response = client.post("/weather", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert b"Missing required fields in the request data." in response.data

def test_get_weather_invalid_city(client):
    response = client.get("/weather/Berlin")
    assert response.status_code == 404
    assert b"Sorry, no weather information available" in response.data
    

def test_update_weather_valid_data(client):
    city = "San Francisco"
    data = {
        "temperature": 16,
        "weather": "Partly Cloudy"
    }
    response = client.put(f"/weather/{city}", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert b"Weather data for San Francisco updated successfully." in response.data

def test_update_weather_invalid_city(client):
    city = "Chicago"
    data = {
        "temperature": 18,
        "weather": "Sunny"
    }
    response = client.put(f"/weather/{city}", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert b"Sorry, no weather information available for Chicago." in response.data

def test_update_weather_invalid_data(client):
    city = "San Francisco"
    data = {
        "temperature": 25
    }
    response = client.put(f"/weather/{city}", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert b"Weather data for San Francisco updated successfully." in response.data
    assert weather_data[city]["temperature"] == 25



def test_update_weather_nonexistent_city(client):
    city = "Denver"
    data = {
        "temperature": 22,
        "weather": "Sunny"
    }
    response = client.put(f"/weather/{city}", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert b"Sorry, no weather information available for Denver." in response.data    
    
    


def test_delete_weather_existing_city(client):
    city = "San Francisco"
    response = client.delete(f"/weather/{city}")
    assert response.status_code == 200
    assert b"Weather data for San Francisco deleted successfully." in response.data

def test_delete_weather_nonexistent_city(client):
    city = "Chicago"
    response = client.delete(f"/weather/{city}")
    assert response.status_code == 404
    assert b"Sorry, no weather information available for Chicago." in response.data

def test_get_deleted_weather_city(client):
    city = "San Francisco"
    response = client.get(f"/weather/{city}")
    assert response.status_code == 404
    assert b"Sorry, no weather information available for San Francisco." in response.data
    
    

