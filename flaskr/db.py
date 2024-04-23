import csv

import click
from flask import current_app, g
import pymysql.cursors


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host='35.232.40.50',
            user='root',
            password='password',
            database='project3',
            port=3306
        )


    return g.db

def close_db(e=None):
    db = g.pop('db', None)

def init_db():
    try:



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


def get_S3Key_from_CSV():
    with open(file="Braden_accessKeys.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        spamreader.__next__()
        _2nd_line = spamreader.__next__().pop()
        s3key = _2nd_line.split(",")[0]
    return s3key;


def get_S3Secret_from_CSV():
    with open(file="Braden_accessKeys.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        spamreader.__next__()
        _2nd_line = spamreader.__next__().pop()
        s3secret = _2nd_line.split(",")[1]
    return s3secret;
