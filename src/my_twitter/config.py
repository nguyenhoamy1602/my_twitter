from logging.config import dictConfig
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Auth:
    CLIENT_ID = (
        "683428721122-827iq5r635c420f8cnjfnnm8u1gq34jn.apps.googleusercontent.com"
    )
    CLIENT_SECRET = "CgioqHSv_2OHDlKA0HITS7Iv"
    REDIRECT_URI = "https://localhost:5000/gCallback"
    AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URI = "https://accounts.google.com/o/oauth2/token"
    USER_INFO = "https://www.googleapis.com/userinfo/v2/me"


class Config(object):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )

    SECRET_KEY = os.environ.get("SECRET_KEY")
    BUCKET_HOST = os.environ.get("BUCKET_HOST")
    BUCKET_ACCESS_KEY = os.environ.get("BUCKET_ACCESS_KEY")
    BUCKET_SECRET_KEY = os.environ.get("BUCKET_SECRET_KEY")
    # BUCKET_SECURE = os.environ.get("MINIO_SECURE")
    BUCKET_NAME = os.environ.get("BUCKET_NAME")

    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_URL = os.environ.get("REDIS_URL")

    REDIS_TWEET = "Tweet"
    REDIS_USER = "User"
    REDIS_FOLLOWER = "Follower"
    REDIS_FOLLOWING = "Following"
