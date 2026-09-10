from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

class Base(DeclarativeBase):
    pass

engine = None
db_session = scoped_session(sessionmaker())

def init_db(app):
    """
    Initializes the engine using parameters managed by config.py,
    binds the scoped session context, and handles automated connection teardowns.
    """
    global engine

    # Pull the exact string processed by your Config class
    database_url = app.config["SQLALCHEMY_DATABASE_URI"]

    engine = create_engine(
        database_url,
        pool_pre_ping=True
    )

    db_session.configure(bind=engine)

    # Clean up sessions automatically at the end of web requests
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
