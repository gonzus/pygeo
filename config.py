import os
from typing import Type


class Config:
    DATABASE_URL_POSTGRES="postgresql://gonzo@localhost:5432/gonzo"
    DATABASE_URL_SQLITE="sqlite:///data.db"

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DATABASE_URL: str = os.getenv("DATABASE_URL", DATABASE_URL_POSTGRES)

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
