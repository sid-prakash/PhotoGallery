import os
import tempfile

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
    help = get_db()
    table = help['project2photos']
    items = table.find({"owner": g.user})

    # Convert items to a list if needed
    items = list(items)
    photo_url = []
    for item in items:
        url = "https://project1s3imagesbucket.s3.us-east-1.amazonaws.com/" + item['photo_url']
        photo_url.append([url, item['photo_url']])
        
    
    if request.method == 'POST':
        file = request.files['fileInput']
        
        filename = secure_filename(file.filename)

        client = boto3.client('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])
        client.put_object(Body=file,
                          Bucket=current_app.config['S3_BUCKET'],
                          Key=filename)
        return render_template('fileupload/gallery.html', image=photo_url, as_attachment=True)
    

    return render_template('fileupload/gallery.html', image=photo_url, as_attachment=True)

@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Download file from S3 bucket to a temporary file
    s3 = boto3.client('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])

    key = os.path.basename(filename)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    s3.download_fileobj( current_app.config['S3_BUCKET'], key, temp_file)

    # Serve the downloaded file
    return send_file(temp_file.name, as_attachment=True, download_name=os.path.basename(filename))