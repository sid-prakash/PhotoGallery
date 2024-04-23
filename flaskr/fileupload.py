import os

from boto3.dynamodb.conditions import Key
from flask import (
    Blueprint, current_app,flash, g, redirect, render_template, request, url_for
)
from google.cloud import storage
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

        db = get_db()


        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tough-craft-420217-626a229abca4.json'  # put json file here
        g.storage_client = storage.Client()

        filename = secure_filename(file.filename)
        table = "INSERT INTO  project3.photos (username, url) VALUES ('"+g.user+"', '"+filename+"');"


        bucket = g.storage_client.get_bucket('422project3')
        blob = bucket.blob(filename)
        blob.upload_from_file(file)

        with db.cursor() as cursor:
            cursor.execute(table)
            db.commit()

        flash("Succes!")
        return render_template('fileupload/index.html')

    return render_template('fileupload/index.html')



