import json

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from my_twitter.auth import login_required
from my_twitter.config import Config
from my_twitter.db import get_db
from my_twitter.minio import MyMinio

bp = Blueprint("tweet", __name__, url_prefix="/auth")


@bp.route("/", methods=["POST", "GET", "PUT", "DELETE"])
@login_required
def handle_tweet():
    db = get_db()
    minio_client = MyMinio.get_minio()

    if request.method == "POST":
        tweet = request.form
        tweet_id = "%s:%s" % (get_id(db, Config.REDIS_TWEET), "user")
        db.hset(Config.REDIS_TWEET, tweet_id, tweet["text"])
        if "pic" in request.files:
            minio_client.upload_pic(Config.MINIO_BUCKET, tweet_id, request.files["pic"])
        return "Tweet created", 201

    elif request.method == "PUT":
        tweet = request.form
        if db.hget(Config.REDIS_TWEET, tweet["id"]):
            db.hset(Config.REDIS_TWEET, tweet["id"], tweet["text"])
            if "pic" in request.files:
                minio_client.upload_pic(
                    Config.MINIO_BUCKET, tweet["id"], request.files["pic"]
                )
            return (
                json.dumps({tweet["id"]: db.hget(Config.REDIS_TWEET, tweet["id"])}),
                201,
            )
        else:
            return "Tweet not found", 404

    elif request.method == "DELETE":
        tweet_id = request.form["id"]
        if db.hdel(Config.REDIS_TWEET, tweet_id):
            return tweet_id + " deleted", 201
        return "Tweet not found", 404

    else:

        return json.dumps({Config.REDIS_TWEET: db.hgetall(Config.REDIS_TWEET)})


def get_id(db, hash_name):
    count = "count"
    if not db.hexists(hash_name, count):
        db.hset(hash_name, count, 1)
    else:
        db.hincrby(hash_name, count)
    return db.hget(hash_name, count)
