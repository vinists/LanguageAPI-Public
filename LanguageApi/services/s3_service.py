import io
import logging
import boto3
from botocore.exceptions import ClientError
import time

from config import Settings, get_settings
settings: Settings = get_settings()


class S3:
    def __init__(self):
        self.s3 = boto3.resource("s3")
        self.bucket = settings.s3_bucket
        self.aws_region = settings.aws_region

    def upload_file(self, data: bytes):
        s3_client = boto3.client('s3')
        try:
            object_name = str(time.time()).split('.')[-1]
            file_obj = io.BytesIO(data)
            s3_client.upload_fileobj(file_obj, self.bucket, object_name)
            return self.get_object_url(object_name)
        except ClientError as e:
            logging.error(e)

    def get_object_url(self, object_name):
        return f"https://{self.bucket}.s3.{self.aws_region}.amazonaws.com/{object_name}"
