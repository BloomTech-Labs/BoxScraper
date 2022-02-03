import os

from boto3.session import Session
from dotenv import load_dotenv


class S3:
    load_dotenv()

    def connect(self):
        return Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        ).client('s3')

    def upload(self, file_path, bucket, file_name):
        self.connect().upload_file(file_path, bucket, file_name)
