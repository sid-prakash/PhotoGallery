from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('fileupload', __name__)

@bp.route('/')
def index():
    d =g
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT photo_url FROM photogallery_data.photo_info WHERE owner=%s', (g.user[0],)
    )
    posts = cursor.fetchall()
    return render_template('fileupload/index.html', posts=posts)