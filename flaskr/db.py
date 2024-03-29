import csv

import click
from boto3.session import Session
from flask import current_app, g
import boto3
from pymongo import MongoClient


def get_db():

    # current_app.config['DYNAMO_TABLES'] = [
    #     {
    #         'TableName': 'project2users',
    #         'KeySchema': [{'AttributeName': 'username', 'KeyType': 'String'}],
    #         'AttributeDefinitions': [{'AttributeName': 'username', 'AttributeType': 'String'}],
    #         'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    #     }, {
    #         'TableName': 'project2photos',
    #         'KeySchema': [{'AttributeName': 'photo_id', 'KeyType': 'number'}],
    #         'AttributeDefinitions': [{'AttributeName': 'photo_id', 'AttributeType': 'number'}],
    #         'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    #     }
    # ]

    # Assuming get_S3Key_from_CSV() and get_S3Secret_from_CSV() are functions to get MongoDB credentials
    mongo_uri = ""
    client = MongoClient(mongo_uri)
    return client["422project2"]

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
