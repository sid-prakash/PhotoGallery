import functools
import boto3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)
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
                db.cursor().execute(
                    "INSERT INTO user_info (username, password_hash) VALUES (\"" + username + "\",\"" + password + "\")"
                )
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

    help = get_db()
    table = help.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )

    return (response['Items'])[0]



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
        elif not user.get('password_hash') == password_hash:
            error = 'Incorrect password.'

        if error is None:
            if session.__len__() != 0:
                session.clear()
            h = session
            session['username'] = username
            return redirect(url_for('fileupload.index'))

        flash(error)


    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    ses = session
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM photogallery_data.user_info WHERE username = %s', (username,)
        )

        g.user = cursor.fetchone()
        user = g.user


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('fileupload.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
