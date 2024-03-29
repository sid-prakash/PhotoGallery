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
                table = db.Table('project2users')
                insert_item_resp = table.put_item(
                    Item={
                        'username': username,
                        'password_hash': password,
                    }
                )
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
#
# @bp.route('/resetpassword', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         password = request.form['password']
#         db = get_db()
#         error = None
#
#
#         if not password:
#             error = 'Password is required.'
#
#         if error is None:
#             try:
#                 table = db.Table('project2users')
#
#                 response = table.update_item(
#                     Key={
#                         'username': g.user,
#                     },
#                     UpdateExpression='SET password_hash = :password_hash',
#                     ExpressionAttributeValues={
#                         ':password_hash': password
#                     }
#                 )
#             except db.IntegrityError:
#                 flash(error)
#             else:
#                 return redirect(url_for("fileupload.gallery"))
#
#         flash(error)
#
#     return render_template('auth/resetpassword.html')

def get_user_info(username):
    table_name = 'project2users'  # Replace 'user_info_table' with your actual table name

    # Assuming app.dynamodb is the initialized DynamoDB resource

    help = get_db()
    table = help[table_name]
    myquery = {"username": username}
    myuser = table.find_one(myquery)


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
        elif not user.get('password_hash') == password_hash:
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
