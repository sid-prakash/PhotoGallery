# Photo Gallery
This is a web application with functions that upload and download images. Images are stored and retrieved from AWS S3, and Google GCP Cloud. The application is also hosted on an AWS EC2 Instance.


## Main Pages
These main pages are behind an authentication wall, where you have to be logged in, to use the gallery or upload a file for your specific account: Additionally, there is a logout button on every screen, you can log out and log in as a different user if you would like.

Image upload: we can choose any photo file to upload
![image](https://github.com/sid-prakash/PhotoGallery/assets/84790796/3fa264e7-ad7c-4fa2-a3ac-6ded0e8bdcf3)

Gallery page: viewing all photos that are attached to the user that logged in
![image](https://github.com/sid-prakash/PhotoGallery/assets/84790796/ae4946cf-eb59-4532-9c44-758fa80347df)

Gallery Search: Use a generic of all photo names on the screen. Client-side search
![image](https://github.com/sid-prakash/PhotoGallery/assets/84790796/d4256514-225b-4866-813f-b33e46976e23)

Gallery download:
![image](https://github.com/sid-prakash/PhotoGallery/assets/84790796/e1ec9270-b48e-4953-9ec4-ede525a4d9dc)

## Run application
To start the application run either **python -m flask --app flask run** or **python3 -m flask --app flask run**
Navigate inside this folder and run **python -m flask --app flaskr/__init__.py run**
To face the app towards the internet add **--host=0.0.0.0**

Our EC2 Instance has the URL ec2-3-87-231-215.compute-1.amazonaws.com:5000
