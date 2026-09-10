from flask.testing import FlaskClient
from core.database import db_session
from sqlalchemy import text
from users.models import UserModel

def test_create_user_db_validation(client: FlaskClient):
    """Asserts that a valid payload registers a 201 response contract."""
    email = "kermit@example.com"
    name = "Kermit the Frog"

    # CHECK: initial creation should succeed
    payload = { "email": email, "name": name }
    response = client.post("/api/users", json=payload)
    assert response.status_code == 201
    json = response.get_json()
    data = json["user"]
    assert data["id"] is not None
    assert data["email"] == "kermit@example.com"
    assert data["name"] == "Kermit the Frog"

    id = data['id']

    # CHECK: should be able to fetch user just created
    response = client.get(f"/api/users/{id}")
    assert response.status_code == 200

    # CHECK: repeated email & name should fail
    response = client.post("/api/users", json=payload)
    assert response.status_code == 400

    # CHECK: repeated email should fail
    payload = { "email": email, "name": "Donald Duck" }
    response = client.post("/api/users", json=payload)
    assert response.status_code == 400

    # CHECK: repeated name should succeed
    payload = { "email": "donald@example.com", "name": name }
    response = client.post("/api/users", json=payload)
    assert response.status_code == 201

    # CHECK: should be able to delete first created user
    response = client.delete(f"/api/users/{id}")
    assert response.status_code == 200

    # CHECK: delete should fail a second time
    response = client.delete(f"/api/users/{id}")
    assert response.status_code == 404

def test_create_user_domain_validation(client: FlaskClient):
    """Asserts that bad data strings are rejected (400)."""
    payload = { "email": "not-a-valid-email", "name": "Miss Piggy" }
    response = client.post("/api/users", json=payload)
    assert response.status_code == 400
    json = response.get_json()
    assert "error" in json
    assert "required" in json["error"]

def test_create_user_duplicate_email_conflict(client: FlaskClient):
    """Asserts that our IntegrityError catch block triggers a clean 400."""
    email = "fozzie@example.com"

    # Seed an initial database model manually
    existing_user = UserModel(email=email, name="Fozzie Bear")
    db_session.add(existing_user)
    db_session.commit()

    # CHECK: Fire an identical request body payload
    payload = { "email": email, "name": "Imposter Fozzie" }
    response = client.post("/api/users", json=payload)
    assert response.status_code == 400
    json = response.get_json()
    assert "error" in json
    assert "already exists" in json["error"]

def test_get_user_not_found(client: FlaskClient):
    """Asserts that querying non-existent ids yields a safe 404."""
    response = client.get("/api/users/9991")
    assert response.status_code == 404

def test_verify_seeded_data(client):
    """Makes sure the migrations seeded some data."""
    count = db_session.execute(text("SELECT COUNT(*) FROM users")).scalar()
    assert count > 0

    count = db_session.execute(text("SELECT COUNT(*) FROM orders")).scalar()
    assert count > 0
