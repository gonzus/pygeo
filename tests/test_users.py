from flask.testing import FlaskClient
from database import db_session
from models.user import UserModel

def test_create_user_success(client: FlaskClient):
    """Asserts that a valid payload registers a 201 response contract."""
    payload = {
        "email": "kermit@example.com",
        "name": "Kermit the Frog"
    }

    response = client.post("/api/users", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] is not None
    assert data["email"] == "kermit@example.com"
    assert data["name"] == "Kermit the Frog"

def test_create_user_pydantic_validation_failure(client: FlaskClient):
    """Asserts that bad data strings are rejected natively at the gate (422)."""
    payload = {
        "email": "not-a-valid-email",
        "name": "Miss Piggy"
    }

    response = client.post("/api/users", json=payload)
    assert response.status_code == 422
    assert "errors" in response.get_json()

def test_create_user_duplicate_email_conflict(client: FlaskClient):
    """Asserts that our IntegrityError catch block triggers a clean 409."""
    # 1. Seed an initial database model manually
    existing_user = UserModel(email="fozzie@example.com", name="Fozzie Bear")
    db_session.add(existing_user)
    db_session.commit()

    # 2. Fire an identical request body payload
    payload = {
        "email": "fozzie@example.com",
        "name": "Imposter Fozzie"
    }
    response = client.post("/api/users", json=payload)

    assert response.status_code == 409
    assert response.get_json()["error"] == "A user with this email already exists."

def test_get_user_not_found(client: FlaskClient):
    """Asserts that querying non-existent ids yields a safe 404."""
    response = client.get("/api/users/9991")
    assert response.status_code == 404
