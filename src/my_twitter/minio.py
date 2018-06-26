from my_twitter import config
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists
from werkzeug.utils import secure_filename
import os


class My_Minio(Minio):
    def __init__(self, minio_host, minio_access_key, minio_secret_key, secure):
        Minio.__init__(
            self,
            minio_host,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=secure,
        )

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
