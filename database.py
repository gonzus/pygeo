from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

class Base(DeclarativeBase):
    pass

# Create a placeholder scoped_session without binding an engine yet
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False
    )
)

# 2. Add a global engine reference that we can populate later
engine = None

def init_db(app):
    """Binds the SQLAlchemy session and engine to the current Flask app's configuration."""

    global engine

    # Grab the URI from the actual initialized app configuration
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")

    connect_args = {"check_same_thread": False} if "sqlite" in db_uri else {}

    # Instantiate the runtime engine
    engine = create_engine(db_uri, connect_args=connect_args)

    # Bind the engine to the existing scoped_session
    db_session.configure(bind=engine)

    # Clean up sessions automatically at the end of web requests
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return engine
