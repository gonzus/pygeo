import os
from typing import Type

class Config:
    DATABASE_URL_PG_DEV="postgresql://gonzo@localhost:5432/gonzo"
    DATABASE_URL_PG_TEST="postgresql://gonzo@localhost:5432/pygeo_test"
    DATABASE_URL_PG_PROD="postgresql://gonzo@localhost:5432/pygeo"
    DATABASE_URL_SQLITE="sqlite:///data.db"

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

class DevConfig(Config):
    DATABASE_URL: str = os.getenv("DATABASE_URL", Config.DATABASE_URL_PG_DEV)
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL

class TestConfig(Config):
    DATABASE_URL: str = os.getenv("DATABASE_URL", Config.DATABASE_URL_PG_TEST)
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL

class ProdConfig(Config):
    DATABASE_URL: str = os.getenv("DATABASE_URL", Config.DATABASE_URL_PG_PROD)
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL
    DEBUG: bool = False

    # In production, Postgres connections require a secure prefix tweak for SQLAlchemy 2.0
    if DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgres://", "postgresql://", 1)

config_by_name: dict[str, Type[Config]] = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}
