import click
from boto3.session import Session
from flask import current_app, g
import boto3
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

    return boto3.resource('dynamodb',
                          region_name='us-east-1',
                          aws_access_key_id='AKIAXCJY6ACWEKKWCBXB',
                          aws_secret_access_key='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')

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
