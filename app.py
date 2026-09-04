import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from config import config_by_name
from database import db_session, engine, Base
from models import UserModel, OrderModel
from views import init_user_blueprint

env = os.getenv("FLASK_ENV", "dev")
migrate = Migrate()

def create_app(config_name: str = "dev") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # 3. Initialize Migrate with your app and your declarative base
    # Since you use a custom engine setup instead of Flask-SQLAlchemy,
    # we pass Base.metadata directly.
    migrate.init_app(app, db=None, metadata=Base.metadata)

    init_user_blueprint(app, "/api/users")

    @app.errorhandler(404)
    def not_found(error: Exception):
        return jsonify({"error": "Resource not found"}), 404

    @app.teardown_appcontext
    def shutdown_session(exception: Exception | None = None) -> None:
        db_session.remove()

    return app

app = create_app(env)

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 5000)),
        debug=app.config.get("DEBUG", True)
    )
