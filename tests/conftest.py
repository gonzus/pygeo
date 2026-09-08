import pytest
from typing import Generator
from flask.testing import FlaskClient
from sqlalchemy import create_engine

from app import create_app
from database import Base, db_session

@pytest.fixture(scope="session")
def app():
    """Configures a temporary test application factory instance."""

    # Spin up an isolated, completely blank in-memory database instance
    test_engine = create_engine("sqlite:///:memory:")

    # Force our globally shared scoped session to connect to this test database
    db_session.configure(bind=test_engine)

    # Initialize the flask context using our 'dev' configurations
    app = create_app("dev")
    app.config.update({
        "TESTING": True,
    })

    # Build all tables up front for the test lifecycle
    Base.metadata.create_all(bind=test_engine)

    yield app

    # Purge the schema entirely at the end of the runtime
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def clean_db(app):
    """Ensures a completely fresh database state before every test."""

    # Clear out any leftover session state from a previous test
    db_session.remove()

    engine = db_session.get_bind()

    # Drop and recreate all tables in-memory
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    # Clean up after the current test completes
    db_session.remove()

@pytest.fixture(scope="function")
def client(app, clean_db) -> Generator[FlaskClient, None, None]:
    """Provides a pristine HTTP client context per individual test."""

    with app.test_client() as test_client:
        yield test_client
