import click
from flask import g
from flask.cli import with_appcontext

from my_twitter import config
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists
from werkzeug.utils import secure_filename
import os

from my_twitter.config import Config


class MyMinio(Minio):
    def __init__(self):
        super().__init__(
            Config.MINIO_HOST,
            access_key=Config.MINIO_ACCESS_KEY,
            secret_key=Config.MINIO_SECRET_KEY,
            secure=False,
        )
        self.create_bucket(Config.MINIO_BUCKET)

    @staticmethod
    def get_minio():
        """Connect to the application's configured database. The connection
        is unique for each request and will be reused if this is called
        again.
        """
        if "minio" not in g:
            g.minio = MyMinio()

        return g.minio

    @staticmethod
    def close_minio(e=None):
        """If this request connected to the database, close the
        connection.
        """
        minio = g.pop("minio", None)
        # minio.close()

    @staticmethod
    def init_minio(self):
        """Clear existing data and create new tables."""
        minio = self.get_minio()
        minio.flushminio()

    @click.command("init-minio")
    @with_appcontext
    def init_minio_command(self):
        """Clear existing data and create new tables."""
        self.init_minio()
        click.echo("Initialized the database.")

    def init_app(self, app):
        """Register database functions with the Flask app. This is called by
        the application factory.
        """
        app.teardown_appcontext(self.close_minio)
        app.cli.add_command(self.init_minio_command)

    def create_bucket(self, name):
        try:
            self.make_bucket(name)
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
        except ResponseError as err:
            raise err

    def save_image(self, bucket, file_name, file_path):
        try:
            self.fput_object(bucket, file_name, file_path)
        except ResponseError as err:
            raise err

    def upload_pic(self, bucket, tweet_id, image):
        image_path = os.path.join(str(os.getcwd()), secure_filename(image.filename))
        image.save(image_path)
        self.save_image(bucket, tweet_id, image_path)
        os.remove(image_path)

    def get_pic(self, bucket, file_name, file_path):
        try:
            self.fget_object(bucket, file_name, file_path)
        except ResponseError as err:
            raise err
