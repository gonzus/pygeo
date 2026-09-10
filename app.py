import os
from flask import Flask
from flask_migrate import Migrate
from config import config_by_name
from core.database import Base, init_db
from core.blueprints import register_all_blueprints

flask_env = os.getenv("FLASK_ENV", "dev")
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    if not config_name:
        config_name = flask_env

    config_class = config_by_name.get(config_name)
    app.config.from_object(config_class)

    init_db(app)

    # Since we aren't using Flask-SQLAlchemy, we pass a dummy 'db' object
    # wrapper that exposes the metadata so Alembic can find our models.
    class SQLAlchemyWrapper:
        metadata = Base.metadata

    migrate.init_app(app, db=SQLAlchemyWrapper(), directory="migrations")

    # Find and register all blueprints.
    register_all_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 5000)),
        debug=app.config.get("DEBUG", True)
    )
