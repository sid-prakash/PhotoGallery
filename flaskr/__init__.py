import os
import csv
from flask import Flask



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )



    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_db()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import fileupload
    app.register_blueprint(fileupload.bp)
    app.add_url_rule('/uploadfile', endpoint='fileupload.index')

    from . import gallery
    app.register_blueprint(gallery.bp)
    app.add_url_rule('/', endpoint='fileupload.gallery')


    app.config['S3_BUCKET'] = "project1s3imagesbucket"
    app.config['S3_KEY'] = get_S3Key_from_CSV()
    app.config['S3_SECRET'] = get_S3Secret_from_CSV()
    app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])

    return app


def get_S3Key_from_CSV():
     with open(file="Braden_accessKeys.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        spamreader.__next__()
        _2nd_line = spamreader.__next__().pop()
        s3key = _2nd_line.split(",")[0]
     return s3key;


def get_S3Secret_from_CSV():
     with open(file="Braden_accessKeys.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        spamreader.__next__()
        _2nd_line = spamreader.__next__().pop()
        s3secret = _2nd_line.split(",")[1]
     return s3secret;