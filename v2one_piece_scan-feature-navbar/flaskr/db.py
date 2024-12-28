#Ajout de la vérification du fichier avant son ouverture pour éviter les erreurs.
#Typage explicite
#Logs explicites

import sqlite3
import os
import click
from flask import current_app, g
from typing import Optional


def get_db() -> sqlite3.Connection:
    """
    Establish and return a connection to the database.
    
    Returns:
        sqlite3.Connection: The database connection.
    """
    if 'db' not in g:
        try:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            current_app.logger.error(f"Database connection failed: {e}")
            raise
    return g.db


def close_db(e: Optional[Exception] = None) -> None:
    """
    Close the database connection at the end of the request lifecycle.

    Args:
        e (Optional[Exception]): Optional error that triggered this call.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db() -> None:
    """
    Initialize the database by executing the schema script.
    """
    db = get_db()

    schema_path = os.path.join(current_app.instance_path, 'text_schema.sql')
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"The schema file '{schema_path}' does not exist.")

    try:
        with current_app.open_resource('text_schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
    except sqlite3.Error as e:
        current_app.logger.error(f"Database initialization failed: {e}")
        raise


@click.command('init-db')
def init_db_command() -> None:
    """
    CLI command to clear existing data and create new tables.
    """
    try:
        init_db()
        click.echo('Initialized the database.')
    except Exception as e:
        click.echo(f"Failed to initialize the database: {e}")


def init_app(app) -> None:
    """
    Register database functions with the Flask app.

    Args:
        app: The Flask application instance.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
