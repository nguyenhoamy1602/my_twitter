import os

from flask import Flask

from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="./static/dist", template_folder="./static")


def main():
    from my_twitter import db
    from my_twitter.config import Config

    from my_twitter.miniodb import MyMinio

    db.init_app(app)
    # create db

    with app.app_context():

        minio_client = MyMinio()
        minio_client.init_app(app)

    from my_twitter import auth, tweet, user

    # register blue print
    app.register_blueprint(auth.bp)
    app.register_blueprint(tweet.bp)
    app.register_blueprint(user.bp)

    app.add_url_rule("/", endpoint="index")
    app.secret_key = Config.SECRET_KEY
    CORS(app)

    app.run()
