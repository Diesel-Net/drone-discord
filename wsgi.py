#!/usr/bin/env python3

"""
WSGI entry point for Gunicorn/Flask


If the environment variable FLASK_APP is not set, the command will try to import 
“app” or “wsgi” (as a “.py” file, or package) and try to detect an application 
instance or factory.

For more information on Flask application auto discovery please visit:
https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery

"""

import api

app = api.create_app()
