import pymongo
import os
import click
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from flask import current_app, g
from flask.cli import with_appcontext
from gridfs import GridFS


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.client = MongoClient(
            host=os.getenv('MONGO_HOST'), 
            port=int(os.getenv('MONGO_PORT')), 
            username=os.getenv('MONGO_INITDB_ROOT_USERNAME'), 
            password=os.getenv('MONGO_INITDB_ROOT_PASSWORD'), 
        )
        g.db = g.client[os.getenv('MONGO_DATABASE')]
        g.fs = GridFS(g.db)
        print(
            f"Mongo: Connecting to `{os.getenv('MONGO_DATABASE')}`"
            f" at ({ os.getenv('MONGO_HOST') }"
            f":{ os.getenv('MONGO_PORT') })"
        )
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    if 'db' in g:
        db = g.pop("db", None)
        client = g.pop("client", None)
        print('Mongo: Database closed')


def init_db(data=None):
    """Create new database file and optionally pre-load json data."""
    get_db()
    g.client.drop_database(os.getenv('MONGO_DATABASE'))
    db = get_db()
    if data != None:
        for key in  data:
            # create collections as defined as "keys" in top level json object
            db[key].insert_many(data[key])


@click.command('init-db')
@click.argument('filename', type=click.Path(exists=True), required=False)
@with_appcontext
def init_db_command(filename=None):
    """Create new database file and optionally pre-load json data."""

    if filename == None:
        init_db()
    else:
        with open(filename, "rb") as fh:
            init_db(json_util.loads(fh.read()))
    print('Mongo: Database initialized')


def register_db(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
