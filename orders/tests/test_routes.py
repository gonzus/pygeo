import pytest
from users.models import UserModel
from orders.models import OrderModel


def test_add_order_to_user_success(client, session):
    """Should successfully create an order when a valid user exists."""
    # Create a real user in the DB using the test session context
    test_user = UserModel(email="test_buyer@example.com", name="Alex Buyer", is_active=True)
    session.add(test_user)
    session.commit()

    # CHECK: first order can be created
    payload = {"amount": 111.11}
    response = client.post(f"/api/orders/user/{test_user.id}", json=payload)
    assert response is not None
    assert response.status_code == 201

    json = response.get_json()
    assert json["status"] == "success"

    data = json["order"]
    assert data["user_id"] == test_user.id
    assert data["amount"] == 111.11
    assert "id" in data

    # CHECK: first order can be retrieved
    check = client.get(f"/api/orders/{data["id"]}", json=payload)
    assert check is not None
    assert check.status_code == 200

    # CHECK: second order can be created
    payload = {"amount": 222.22}
    response = client.post(f"/api/orders/user/{test_user.id}", json=payload)
    assert response is not None
    assert response.status_code == 201

    json = response.get_json()
    assert json["status"] == "success"

    data = json["order"]
    assert data["user_id"] == test_user.id
    assert data["amount"] == 222.22
    assert "id" in data

    # CHECK: second order can be retrieved
    check = client.get(f"/api/orders/{data["id"]}", json=payload)
    assert check is not None
    assert check.status_code == 200

    # CHECK: both orders can be retrieved for the user
    response = client.get(f"/api/orders/user/{test_user.id}", json=payload)
    assert response is not None
    assert response.status_code == 200

    json = response.get_json()
    assert isinstance(json, list)
    assert len(json) == 2
    assert json[0]["amount"] == 111.11
    assert json[1]["amount"] == 222.22

def test_add_order_to_user_fails_user_not_found(client):
    """Should return a 400 error if trying to add an order to a non-existent user id."""
    # CHECK: hit a random user ID that definitely doesn't exist
    payload = {"amount": 25.00}
    response = client.post("/api/orders/user/999999", json=payload)
    assert response.status_code == 400

    json = response.get_json()
    assert "error" in json
    assert "is inactive or does not exist" in json["error"]


def test_add_order_to_user_fails_invalid_amount(client, session):
    """Should return a 400 error if the order amount is zero or negative."""
    # 1. Arrange: Create a valid user
    test_user = UserModel(email="valid_user@example.com", name="Valid User", is_active=True)
    session.add(test_user)
    session.commit()

    # 2. Act: Try to pass a negative amount payload
    payload = {"amount": -10.50}
    response = client.post(f"/api/orders/user/{test_user.id}", json=payload)

    # 3. Assert: Verify the business validation layer catches it
    assert response.status_code == 400

    json = response.get_json()
    assert "error" in json
    assert "greater than zero" in json["error"]
