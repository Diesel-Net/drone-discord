from flask import Flask
from api.drone import receive_events
from api.mongo import register_db

# we want the configuration passed in as a parameter here so that we
# can easily change the configuration during runtime, e.g. for unit tests
def create_app():
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    # register the database cli commands
    register_db(app)

    # import/register endpoints
    app.register_blueprint(receive_events)

    return app
