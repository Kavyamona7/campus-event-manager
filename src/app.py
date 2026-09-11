from flask import Flask

from services.mongo_service import MongoService
from routes.dashboard import dashboard_bp
from routes.events import events_bp
from routes.users import users_bp
from routes.analytics import analytics_bp

def create_app():
    app = Flask(__name__)

    # Initialize MongoDB
    mongo = MongoService()
    mongo.ping()

    app.config["MONGO_SERVICE"] = mongo

    # Register routes
    app.register_blueprint(
        dashboard_bp
    )
    app.register_blueprint(
        events_bp
    )
    app.register_blueprint(users_bp)
    app.register_blueprint(analytics_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)