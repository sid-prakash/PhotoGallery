import mysql.connector
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host='35.232.40.50',
            user='root',
            password='password',
            database='Google_Cloud_SQL',
            port=3306
        )


    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    try:
        db = get_db()
        db.close()


        print('Connected to the database.')
    except Exception as e:
        print(f'Failed to connect to the database: {e}')

@click.command('init-db')
def init_db_command():
    """Connect to the existing database."""
    init_db()
    print('Connected to the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
