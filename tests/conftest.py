import pytest
from typing import Generator
from flask.testing import FlaskClient
from sqlalchemy import create_engine, text
import os


from app import create_app
from database import Base, db_session

@pytest.fixture(scope="session")
def app():
    """Configures a temporary test application factory instance running on Postgres."""

    # 1. Pull a dedicated test DB URL from your environment (Never use your production DB!)
    # Defaulting to a local postgres instance named 'my_app_test'
    test_db_url = os.getenv("TEST_DATABASE_URL", "postgresql://gonzo@localhost:5432/gonzo")
    test_engine = create_engine(test_db_url, echo=True).execution_options(
        schema_translate_map={None: "pygeo_test"}
    )


    # 2. Safely create the test schema if it doesn't exist yet
    with test_engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS pygeo_test;"))
        conn.commit()

    # 3. Configure the scoped session to bind to the engine AND use the test schema
    # The schema_translate_map tells SQLAlchemy to redirect None (default public schema) to 'pygeo_test'
    db_session.configure(
        bind=test_engine,
    )

    # Initialize the flask context using our 'dev' configurations
    app = create_app("dev")
    app.config.update({
        "TESTING": True,
    })

    # 5. Build all tables inside the 'pygeo_test' schema
    Base.metadata.create_all(bind=test_engine)

    yield app

    # 6. Purge the schema entirely at the end of the runtime to keep dev clean
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
