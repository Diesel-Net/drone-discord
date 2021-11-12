from flask import Flask
from api.drone import drone_events
from api.mongo import register_db
from api.health import health_check

# we want the configuration passed in as a parameter here so that we
# can easily change the configuration during runtime, e.g. for unit tests
def create_app():
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    # register the database and it's cli commands
    register_db(app)

    # register listening endpoints
    app.register_blueprint(drone_events)
    app.register_blueprint(health_check)

    return app
