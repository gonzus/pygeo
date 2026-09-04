import os
from flask import Flask, jsonify
from config import config_by_name
from database import db_session, engine, Base
from models import UserModel, OrderModel
from views import init_user_blueprint

env = os.getenv("FLASK_ENV", "dev")

def create_app(config_name: str = "dev") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    init_user_blueprint(app, "/api/users")

    @app.errorhandler(404)
    def not_found(error: Exception):
        return jsonify({"error": "Resource not found"}), 404

    @app.teardown_appcontext
    def shutdown_session(exception: Exception | None = None) -> None:
        db_session.remove()

    if config_name == "dev":
        with app.app_context():
            Base.metadata.create_all(bind=engine)

    return app

app = create_app(env)

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 5000)),
        debug=app.config.get("DEBUG", True)
    )
