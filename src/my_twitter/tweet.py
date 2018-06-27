import json

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from my_twitter.config import Config
from my_twitter.db import get_db
from my_twitter.minio import MyMinio

bp = Blueprint("tweet", __name__)


@bp.route("/tweet", methods=["POST", "GET", "PUT", "DELETE"])
def handle_tweet():
    db = get_db()
    minio_client = MyMinio.get_minio()
    hash_name = "Tweet"
    count = "count"

    if request.method == "POST":
        tweet = request.form
        if not db.hexists(hash_name, count):
            db.hset(hash_name, count, 1)
        else:
            db.hincrby(hash_name, count)
        tweet_id = "%s:%s" % (db.hget(hash_name, count), "user")
        db.hset(hash_name, tweet_id, tweet["text"])
        if "pic" in request.files:
            minio_client.upload_pic(Config.MINIO_BUCKET, tweet_id, request.files["pic"])
        return "Tweet created", 201

    elif request.method == "PUT":
        tweet = request.form
        if db.hget(hash_name, tweet["id"]):
            db.hset(hash_name, tweet["id"], tweet["text"])
            if "pic" in request.files:
                minio_client.upload_pic(
                    Config.MINIO_BUCKET, tweet["id"], request.files["pic"]
                )
            return json.dumps({tweet["id"]: db.hget(hash_name, tweet["id"])}), 201
        else:
            return "Tweet not found", 404

    elif request.method == "DELETE":
        tweet_id = request.form["id"]
        if db.hdel(hash_name, tweet_id):
            return tweet_id + " deleted", 201
        return "Tweet not found", 404

    else:

        return json.dumps({hash_name: db.hgetall(hash_name)})
