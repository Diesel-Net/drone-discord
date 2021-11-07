from .config import _config
from .logger import logger
import connexion
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ruamel import yaml
from api.endpoints import (
    log
)
from api import (
    database,
)

# we want the configuration passed in as a parameter here so that we
# can easily change the configuration during runtime, e.g. for unit tests
def create_app(config=_config):
    """Create and configure an instance of the Flask application."""

    connexion_app = connexion.FlaskApp(
        __name__,
        options={'swagger_ui': False},
        port=5000,
    )

    app = connexion_app.app

    app.config.update(config)

    # Enable CORS (Cross Origin Resource Sharing)
    CORS(app)

    # register the database cli commands
    database.register(app)

    # import/register endpoints
    app.register_blueprint(log.bp)


    # TODO - Move rate limiting responsibility to Traefik v2
    global throttle
    throttle = Limiter(
        app,
        # rate limit by remote address of request
        key_func=get_remote_address,
        # values are set rediculously high until testing can be done
        default_limits=[
            f'{ app.config["GLOBAL_RATE_PER_DAY"]} per day',
            f'{ app.config["GLOBAL_RATE_PER_HOUR"]} per hour',
            f'{ app.config["GLOBAL_RATE_PER_MINUTE"]} per minute',
        ],
    )

    return connexion_app


def on_startup():
    #logger.debug('Executing startup routine...')
    pass
