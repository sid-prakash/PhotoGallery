import os
import tempfile
from google.cloud import storage
from boto3.dynamodb.conditions import Key, Attr
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for, send_from_directory, send_file
)
from pymongo import collection
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
import boto3

bp = Blueprint('gallery', __name__)

@bp.route('/index')
def index():

    return render_template('fileupload/index.html')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM project3.photos WHERE username='"+g.user+"';")
        items = cursor.fetchall()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tough-craft-420217-626a229abca4.json' #put json file here
    g.storage_client = storage.Client()

    # Convert items to a list if needed
    items = list(items)
    photo_url = []
    for item in items:
        url = "https://storage.cloud.google.com/422project3/" + item['url']
        photo_url.append([url, item['url']])

    

    return render_template('fileupload/gallery.html', image=photo_url, as_attachment=True)


def download_file_from_bucket(blob_name,file_path,bucket_name):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tough-craft-420217-626a229abca4.json'  # put json file here
    g.storage_client = storage.Client()
    try:
        bucket = g.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path,'wb') as f:
            g.storage_client.download_blob_to_file(blob,f)
        return(True)
    except Exception as e:
        print (e)
        return False


@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Download file from S3 bucket to a temporary file
    #s3 = boto3.client('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])

    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tough-craft-420217-626a229abca4.json' #put json file here
    g.storage_client = storage.Client()

    bucket = '422project3'
    blobname = filename
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    download_file_from_bucket(blobname, temp_file, bucket)

    # Serve the downloaded file
    return send_file(temp_file.name, as_attachment=True, download_name=os.path.basename(filename))

    