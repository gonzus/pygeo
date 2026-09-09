import os
from flask import Flask
from flask_migrate import Migrate
from config import config_by_name
from database import init_db, Base
from views import init_user_blueprint

flask_env = os.getenv("FLASK_ENV", "dev")
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    if not config_name:
        config_name = flask_env

    app.config.from_object(config_by_name[config_name])

    # 2. Initialize your database engine
    engine = init_db(app)

    # TODO: evaluate whether we should get rid of this.
    # Since you aren't using Flask-SQLAlchemy, we pass a dummy 'db' object wrapper
    # or pass a custom object that exposes the metadata so Alembic can find your models.
    class SQLAlchemyWrapper:
        metadata = Base.metadata

    migrate.init_app(app, db=SQLAlchemyWrapper(), directory="migrations")

    init_user_blueprint(app, "/api/users")

    return app

if __name__ == "__main__":
    app = create_app(flask_env)
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 5000)),
        debug=app.config.get("DEBUG", True)
    )
