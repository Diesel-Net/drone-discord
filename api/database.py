import pymongo
import os
import click
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from flask import (
    current_app,
    g,
)
from flask.cli import with_appcontext
from api import logger
from gridfs import GridFS

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:

        if 'DATABASE_USER' in current_app.config:
            g.client = MongoClient(
                host=current_app.config['DATABASE_HOST'], 
                port=current_app.config['DATABASE_PORT'],
                username=current_app.config['DATABASE_USER'],
                password=current_app.config['DATABASE_PASSWORD'],
            )
        else:
            # no creds... For automated testing?
            # TODO: come back to this
            g.client = MongoClient(
                'localhost', 
                27017,
            )

        g.db = g.client[current_app.config['DATABASE']]
        g.fs = GridFS(g.db)
        
        logger.debug(
            f'Database opened ({ current_app.config["DATABASE_HOST"] }:{ current_app.config["DATABASE_PORT"] })'
        )

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    if 'db' in g:
        db = g.pop("db", None)
        client = g.pop("client", None)

        logger.debug("Database closed")


def init_db(data=None):
    """Create new database file and optionally pre-load json data."""

    get_db()
    g.client.drop_database(current_app.config['DATABASE'])
    db = get_db()

    
    if data != None:
        for key in  data:
            # create collections as defined as "keys" in top level json object
            db[key].insert_many(data[key])


@click.command("init-db")
@click.argument('filename', type=click.Path(exists=True), required=False)
@with_appcontext
def init_db_command(filename=None):
    """Create new database file and optionally pre-load json data."""

    if filename == None:
        init_db()
    else:
        with open(filename, "rb") as fh:
            init_db(json_util.loads(fh.read()))
            
    #click.echo("Database initialized")
    logger.info("Database initialized")


def register(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
