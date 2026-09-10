import pytest
from flask_migrate import upgrade as flask_migrate_upgrade
from sqlalchemy import MetaData, event
from app import create_app
from core import database


@pytest.fixture(scope="session")
def app():
    """Initializes the Flask application instance configured for testing."""
    # This forces the factory to build using the test config
    app = create_app("test")

    # Safety Guard Check (Reads the newly initialized engine URL)
    db_uri = str(database.engine.url)
    if not db_uri.endswith("/pygeo_test") and not db_uri.endswith("sqlite:///:memory:"):
        pytest.exit(
            f"\n❌ [CRITICAL SAFETY FAILURE]: Target database is dangerous! "
            f"Expected URI ending in '/pygeo_test', but got '{db_uri}'. "
            f"Aborting execution to protect production/development data."
        )

    return app


@pytest.fixture(scope="session", autouse=True)
def setup_database(app):
    """Runs ONCE for the entire test session."""
    with app.app_context():
        # Executes your migration scripts against the fresh test DB
        flask_migrate_upgrade()

    yield

    # Global Teardown: Use the metadata of the dynamically configured engine
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=database.engine)
        metadata.drop_all(bind=database.engine)


@pytest.fixture(scope="function")
def session(app):
    """Wraps the test inside a Postgres SAVEPOINT transaction and rolls it back."""
    with app.app_context():
        connection = database.engine.connect()
        transaction = connection.begin()

        database.db_session.configure(bind=connection)
        nested = connection.begin_nested()

        @event.listens_for(database.db_session, "after_transaction_end")
        def restart_savepoint(session, trans):
            nonlocal nested
            if trans.nested and not nested.is_active:
                nested = connection.begin_nested()

        yield database.db_session

        database.db_session.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(app, session):
    """A test client fixture that forces the application endpoints to share transactions."""
    return app.test_client()
