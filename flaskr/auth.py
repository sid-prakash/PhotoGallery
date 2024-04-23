import functools
import boto3
import sqlalchemy
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
import pymysql.cursors
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from boto3.dynamodb.conditions import Key

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                with db.cursor() as cursor:
                    cursor.execute("INSERT INTO project3.users (username, password) VALUES ('"+username+"', '"+password+"');")
                    db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

def get_user_info(username):
    table_name = 'project2users'  # Replace 'user_info_table' with your actual table name

    # Assuming app.dynamodb is the initialized DynamoDB resource

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM project3.users WHERE username='"+username+"';")
        myuser = cursor.fetchone()


    return myuser



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_hash = request.form['password']
        error = None

        user = get_user_info(username)

        print(user)



        if user is None:
            error = 'Incorrect username.'
        elif not user['password'] == password_hash:
            error = 'Incorrect password.'

        if error is None:
            if session.__len__() != 0:
                session.clear()
            h = session
            session['username'] = username
            return redirect(url_for("fileupload.gallery"))

        flash(error)


    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    ses = session
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = username


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('fileupload.gallery'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
