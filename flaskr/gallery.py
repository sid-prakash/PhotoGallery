from boto3.dynamodb.conditions import Key, Attr
from flask import (
    Blueprint, current_app,flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
import boto3

bp = Blueprint('gallery', __name__)

@bp.route('/')
@login_required
def upload_file():
    help = get_db()
    table = help.Table('project2photos')
    username = g.user
    response = table.scan(
        FilterExpression=Attr('owner').eq(g.user)
    )
    
    items = response['Items']
    photo_url = []
    for item in items:
        url = "https://project1s3imagesbucket.s3.us-east-1.amazonaws.com/" + item['photo_url']
        photo_url.append([url, item['photo_url']])
    

    return render_template('fileupload/gallery.html', image=photo_url, as_attachment=True)