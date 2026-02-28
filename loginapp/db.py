"""PostgreSQL database connectivity for Flask web app."""
from flask import Flask, g
import psycopg2
import psycopg2.extras

connection_params = {}

def init_db(app: Flask, user: str, password: str, host: str, database: str,
            port: int = 5432, autocommit: bool = True):
    """Sets up PostgreSQL connectivity for the specified Flask app."""
    connection_params['user'] = user
    connection_params['password'] = password
    connection_params['host'] = host
    connection_params['database'] = database
    connection_params['port'] = port
    connection_params['autocommit'] = autocommit
    app.teardown_appcontext(close_db)

def get_db():
    """Gets a PostgreSQL database connection for the current Flask request."""
    if 'db' not in g:
        conn = psycopg2.connect(
            user=connection_params['user'],
            password=connection_params['password'],
            host=connection_params['host'],
            dbname=connection_params['database'],
            port=connection_params['port']
        )
        conn.autocommit = connection_params.get('autocommit', True)
        g.db = conn
    return g.db

def get_cursor():
    """Gets a new PostgreSQL dictionary cursor."""
    return get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db(exception=None):
    """Closes the PostgreSQL database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()