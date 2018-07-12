import os

from flask import Flask

from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="./static/dist", template_folder="./static")


def create_app():
    from my_twitter.config import Config

    app.config.from_object(Config)

    from my_twitter import db
    from my_twitter import my_s3

    db.init_app(app)
    with app.app_context():
        my_s3.init_s3()

    from my_twitter import auth, tweet, user

    # register blue print
    app.register_blueprint(auth.bp)
    app.register_blueprint(tweet.bp)
    app.register_blueprint(user.bp)

    app.add_url_rule("/api", endpoint="index")
    # app.secret_key = Config.SECRET_KEY
    CORS(app, resources=r"/api/*")
    app.config["CORS_HEADERS"] = "Content-Type"


def main():
    create_app()
    app.run(host="0.0.0.0", port=50022)
