from boto3.dynamodb.conditions import Key
from flask import (
    Blueprint, current_app,flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
import boto3

bp = Blueprint('fileupload', __name__)

'''
@bp.route('/')
@login_required
def index():
    d = g
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT photo_url FROM photogallery_data.photo_info WHERE owner=%s', (g.user[0],)
    )
    posts = cursor.fetchall()
    return render_template('fileupload/index.html', posts=posts)
'''


@bp.route('/', methods=['POST'])
@login_required
def upload_file():
    # cur = conn.cursor()
    print("woowowowowow")
    if request.method == 'POST':
        print("woowowowowow")
        file = request.files['fileInput']
        
        filename = secure_filename(file.filename)

        client = boto3.client('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])
        client.put_object(Body=file,
                          Bucket=current_app.config['S3_BUCKET'],
                          Key=filename)
        

        return render_template('fileupload/gallery.html')

    return render_template('fileupload/gallery.html')



