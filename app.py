from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import boto3

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
# conn = connection to DB

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
app.config['S3_KEY'] = "AWS_ACCESS_KEY"
app.config['S3_SECRET'] = "AWS_ACCESS_SECRET"
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])

s3 = boto3.client(
    's3',
    aws_access_key_id=app.config['S3_KEY'],
    aws_secreat_access_key=app.config['S3_SECRET']
)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # cur = conn.cursor()
    if request.method == 'POST':
        file = request.files['img']
        if not allowed_file(file.filename):
                return "FILE NOT ALLOWED!"
        
        filename = secure_filename(file.filename)
        print(filename)


        s3_resource = boto3.resource("s3")
        s3_resource.Bucket(app.config['S3_BUCKET']).upload_fileobj(file, filename)

        # cur.execute('INSERT INTO TABLE(IMAGE_ID, IMAGE, IMAGE_NAME))
        # cur.commit()
        
        # return render_template('index.html', img=img)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()