import pytest
from typing import Generator
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
def client(app) -> Generator[FlaskClient, None, None]:
    """Provides a pristine HTTP client context per individual test."""
    with app.test_client() as test_client:
        yield test_client

    # Crucial: Roll back any modifications made by a single test function 
    # to prevent data leaking into subsequent tests
    db_session.rollback()
    # Explicitly clear out rows to ensure a clean state
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
