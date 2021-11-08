from flask import Flask
from api.endpoints import log
from api import database

# we want the configuration passed in as a parameter here so that we
# can easily change the configuration during runtime, e.g. for unit tests
def create_app():
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    # register the database cli commands
    database.register(app)

    # import/register endpoints
    app.register_blueprint(log.bp)

    return app
