import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from config import config_by_name

# Enforce clean typing base layer
class Base(DeclarativeBase):
    pass

# Initialize configurations based on environment
env = os.getenv("FLASK_ENV", "dev")
current_config = config_by_name[env]

# Create the engine context
engine = create_engine(
    current_config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False} if "sqlite" in current_config.SQLALCHEMY_DATABASE_URI else {}
)

# Create the thread-safe scoped session
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

# Bind query properties for traditional model lookups
Base.query = db_session.query_property()
