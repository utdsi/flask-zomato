import pytest
import json
from index import app,menu,orders


@pytest.fixture(autouse=True)
def clean_menu():
    
    menu = []


def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_add_dish_route():
    client = app.test_client()
    dish_data = {
        "dish_name": "Pizza",
        "price": "9.99",
        "availability": "true"
    }
    response = client.post("/add_dish", data=dish_data)
    assert response.status_code == 302
    assert len(menu) == 1
    assert menu[0]["name"] == "Pizza"

def test_remove_dish_route():
    client = app.test_client()
    menu.append({"id": 1, "name": "Pizza", "price": 9.99, "availability": True})
    dish_data = {
        "dish_id": 1
    }
    response = client.post("/remove_dish", data=dish_data)
    assert response.status_code == 302
    assert len(menu) == 0

def test_update_availability_route():
    client = app.test_client()
    dish_data = {
        "dish_id": 1,
        "availability": "true"
    }
    response = client.post("/update_availability", data=dish_data)
    assert response.status_code == 302
    assert menu[0]["availability"] is True

def test_place_order_route_valid_selection():
    client = app.test_client()
    menu.append({"id": 1, "name": "Pizza", "price": 9.99, "availability": True})
    menu.append({"id": 2, "name": "Burger", "price": 5.99, "availability": True})
    dish_data = {
        "customer_name": "John Doe",
        "dish_id": [1, 2]
    }
    response = client.post("/place_order", data=dish_data)
    assert response.status_code == 200
    assert len(orders) == 1
    assert orders[0]["customer_name"] == "John Doe"
    assert orders[0]["status"] == "received"

def test_place_order_route_invalid_selection():
    client = app.test_client()
    dish_data = {
        "customer_name": "John Doe",
        "dish_id": [1, 2]
    }
    menu.append({"id": 1, "name": "Pizza", "price": 9.99, "availability": False})
    menu.append({"id": 2, "name": "Burger", "price": 5.99, "availability": True})
    response = client.post("/place_order", data=dish_data)
    assert response.status_code == 200
    assert len(orders) == 0