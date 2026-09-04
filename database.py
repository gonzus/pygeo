import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from config import config_by_name

class Base(DeclarativeBase):
    pass

env = os.getenv("FLASK_ENV", "dev")
current_config = config_by_name[env]

engine = create_engine(
    current_config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False} if "sqlite" in current_config.SQLALCHEMY_DATABASE_URI else {}
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base.query = db_session.query_property()
