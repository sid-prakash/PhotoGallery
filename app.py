from flask import Flask, render_template, url_for, request, redirect, send_file
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import mysql.connector
import boto3


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.debug = True

#We have to make a connection to the database. There is almost certainly some "bad practice" going on here (but it will work)
db = mysql.connector.connect(host='se422project1.cfcmskqwgqu4.us-east-1.rds.amazonaws.com',
        user='admin',
        password='password',
        db='photogallery_data',
        port = '3306')

#We must create a cursor object. It will let us execute all the queries we want
cursor_conn = db.cursor()




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return 'Successfully logged in'
    return render_template('login.html', error=error)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['S3_BUCKET'] = "project1s3imagesbucket"
app.config['S3_KEY'] = "AKIAXCJY6ACWGBTNMSXF"
app.config['S3_SECRET'] = "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"
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # cur = conn.cursor()
    
    if request.method == 'POST':
        file = request.files['img']
        if not allowed_file(file.filename):
                return "FILE NOT ALLOWED!"
        
        filename = secure_filename(file.filename)
        content_type = request.mimetype
        print(filename)

        client = boto3.client('s3', aws_access_key_id=app.config['S3_KEY'], aws_secret_access_key=app.config['S3_SECRET'])
        client.put_object(Body=file,
                          Bucket=app.config['S3_BUCKET'],
                          Key=filename)


    if request.method == 'GET':
        if 'fileNameToSearch' in request.args:
            s3objectkey = request.args.get('fileNameToSearch')
            client = boto3.client('s3', aws_access_key_id = app.config['S3_KEY'], aws_secret_access_key = app.config['S3_SECRET'])
            image = client.get_object(Bucket=app.config['S3_BUCKET'], Key=s3objectkey)
            image_data = image.get('Body').read()

            return send_file(BytesIO(image_data),mimetype='jpeg', download_name=s3objectkey)

        
    return render_template('index.html')

@app.route('/returnpic', methods=['GET','POST'])
def returnpic():
    client = boto3.client('s3',aws_access_key_id=app.config['S3_KEY'], aws_secret_access_key=app.config['S3_SECRET'])
    return send_file('NathanielBorenstein.jpg')

@app.route('/ret_image_file', methods=['GET'])
def ret_image_file():
    client = boto3.client('s3',aws_access_key_id=app.config['S3_KEY'], aws_secret_access_key=app.config['S3_SECRET'])
    image = client.get_object(Bucket=app.config['S3_BUCKET'], Key='woods.jpg')
    image_data = image.get('Body').read()
    #This took me 7 hours to figure out
    return send_file(BytesIO(image_data),mimetype='jpeg', download_name='woods.jpg')


@app.route('/retrieve_images', methods=['GET', 'POST'])
def retrieve_images():
    return render_template('retrieve_images.html')

@app.route('/',methods=['GET'])
def image_from_string():
    print(request.args)
    print(type(request.args))

    client = boto3.client('s3', aws_access_key_id = app.config['S3_KEY'], aws_secret_access_key = app.config['S3_SECRET'])
    image = client.get_object(Bucket=app.config['S3_BUCKET'], Key='woods.jpg')
    image_data = image.get('Body').read()
    return send_file(BytesIO(image_data),mimetype='jpeg', download_name='woods.jpg')


@app.route('/makeaquery', methods=['GET'])
def makingthequery():
    cursor_conn.execute("SELECT * FROM photogallery_data.photo_info WHERE owner = 'ellie'")
    for row in cursor_conn.fetchall():
        print(row[0])

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
