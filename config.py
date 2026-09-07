import os
from typing import Type

class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-123")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///data.db",
    )

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = Config.DATABASE_URL

class ProdConfig(Config):
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = Config.DATABASE_URL
    # In production, Postgres connections require a secure prefix tweak for SQLAlchemy 2.0
    if Config.DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = Config.DATABASE_URL.replace("postgres://", "postgresql://", 1)

config_by_name: dict[str, Type[Config]] = {
    "dev": DevConfig,
    "prod": ProdConfig
}
