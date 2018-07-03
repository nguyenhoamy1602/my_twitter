import boto3
import click
from botocore.client import Config
from botocore.errorfactory import ClientError
from flask import g
from my_twitter.cli import app


def get_s3():
    if "s3" not in g:
        g.s3 = boto3.client(
            "s3",
            endpoint_url=app.config["BUCKET_HOST"],
            aws_access_key_id=app.config["BUCKET_ACCESS_KEY"],
            aws_secret_access_key=app.config["BUCKET_SECRET_KEY"],
            config=Config(signature_version="s3v4"),
            region_name="ap-northeast-1",
        )
    return g.s3


def upload(file, key):
    get_s3()
    g.s3.upload_fileobj(file, app.config["BUCKET_NAME"], key)


def delete(key):
    g.s3.delete_object(Bucket=app.config["BUCKET_NAME"], Key=key)


#
# def download(file, path):
#     g.s3.Bucket(BUCKET_NAME).download_file(file, path)
#
#
# def get_image(key):
#     return g.s3.Bucket(BUCKET_NAME).get_object(Key=key)


def get_presigned_url(key):
    get_s3()
    return g.s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": app.config["BUCKET_NAME"], "Key": key},
    )


# def create_bucket():
#     try:
#         g.s3.create_bucket(ACL='public-read', Bucket=BUCKET_NAME)
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
#             pass


def init_s3():
    get_s3()
    # create_bucket()
