import os
from typing import Type


class Config:
    DATABASE_URL_PG_DEV = "postgresql://gonzo@localhost:5432/gonzo"
    DATABASE_URL_PG_TEST = "postgresql://gonzo@localhost:5432/pygeo_test"
    DATABASE_URL_PG_PROD = "postgresql://gonzo@localhost:5432/pygeo"
    DATABASE_URL_SQLITE = "sqlite:///data.db"

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    @staticmethod
    def _normalize_uri(uri: str) -> str:
        """Ensures legacy 'postgres://' URLs match SQLAlchemy 2.0 requirements."""
        if uri.startswith("postgres://"):
            return uri.replace("postgres://", "postgresql://", 1)
        return uri


class DevConfig(Config):
    # Evaluated at class load time, defaulting safely to development
    db_url: str = os.getenv("DATABASE_URL", Config.DATABASE_URL_PG_DEV)
    SQLALCHEMY_DATABASE_URI: str = Config._normalize_uri(db_url)
    DEBUG: bool = True
    TESTING: bool = False


class TestConfig(Config):
    # Read from a dedicated TEST_DATABASE_URL if available, or fallback to the
    # standard DATABASE_URL, then the safe hardcoded string. This prevents an
    # active prod / dev DATABASE_URL envvar from leaking into tests.
    db_url: str = os.getenv(
        "TEST_DATABASE_URL",
        os.getenv("DATABASE_URL", Config.DATABASE_URL_PG_TEST)
    )
    SQLALCHEMY_DATABASE_URI: str = Config._normalize_uri(db_url)
    DEBUG: bool = False
    TESTING: bool = True


class ProdConfig(Config):
    db_url: str = os.getenv("DATABASE_URL", Config.DATABASE_URL_PG_PROD)
    SQLALCHEMY_DATABASE_URI: str = Config._normalize_uri(db_url)
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,  # Checks if database dropped connection before trying to query
        "pool_recycle": 1800,   # Recycles connections every 30 minutes to prevent staleness
    }

    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")


config_by_name: dict[str, Type[Config]] = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}
