import flask_s3
from flask_app import app
flask_s3.create_all(app, bucket_name='brstatic')