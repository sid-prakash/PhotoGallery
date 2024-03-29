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


# @bp.route('/')
# @login_required
# def index():
#
#     return render_template('fileupload/index.html')


import random






@bp.route('/fileupload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['fileInput']
        
        filename = secure_filename(file.filename)
        table = get_db().Table('project2photos')
        insert_item_resp = table.put_item(
            Item={
                'photo_id': random.randint(0,500),
                'photo_url': filename,
                'owner': g.user,
            }
        )

        client = boto3.client('s3', aws_access_key_id=current_app.config['S3_KEY'], aws_secret_access_key=current_app.config['S3_SECRET'])
        client.put_object(Body=file,
                          Bucket=current_app.config['S3_BUCKET'],
                          Key=filename)



        flash("Succes!")
        return render_template('fileupload/index.html')

    return render_template('fileupload/index.html')



