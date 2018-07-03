import redis

import click
from flask import current_app, g
from flask.cli import with_appcontext
from my_twitter.config import Config


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = redis.Redis(
            host=Config.REDIS_URL, port=Config.REDIS_PORT, db=0, decode_responses=True
        )

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)
    # db.close()


def init_db():
    """Clear existing data and create new tables."""
    get_db().flushall()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
