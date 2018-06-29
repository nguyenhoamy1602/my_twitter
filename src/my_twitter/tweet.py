import json

from flask import Blueprint, g, request, jsonify

from my_twitter.config import Config
from my_twitter.db import get_db
from my_twitter.miniodb import MyMinio
from my_twitter.models import User

bp = Blueprint("tweet", __name__, url_prefix="/tweet")


@bp.route("/", methods=["POST", "GET", "PUT", "DELETE"])
# @login_required
def handle_tweet():
    db = get_db()
    minio_client = MyMinio.get_minio()

    if request.method == "PUT":
        tweet = request.form
        user_id = tweet["id"].split(":")[1]
        if user_id == g.user_id and db.hget(Config.REDIS_TWEET, tweet["id"]):
            db.hset(Config.REDIS_TWEET, tweet["id"], tweet["text"])
            if "pic" in request.files:
                minio_client.upload_pic(
                    Config.MINIO_BUCKET, tweet["id"], request.files["pic"]
                )
            return jsonify({tweet["id"]: db.hget(Config.REDIS_TWEET, tweet["id"])})

        else:
            return "Tweet not found", 404

    elif request.method == "DELETE":
        tweet_id = request.form["id"]
        if db.hdel(Config.REDIS_TWEET, tweet_id):
            return tweet_id + " deleted", 201
        return "Tweet not found", 404

    else:
        tweet_list = []
        for i in db.hgetall(Config.REDIS_TWEET):
            if i != "count":
                tweet_list.append(User.tweet_jsonify(i))
        return jsonify(tweet_list)


@bp.route("/post", methods=["POST"])
# @login_required
def post_tweet():
    db = get_db()
    minio_client = MyMinio.get_minio()
    tweet = request.form
    tweet_id = "%s:%s" % (get_id(db, Config.REDIS_TWEET), "108954821222298556249")
    db.hset(Config.REDIS_TWEET, tweet_id, tweet["text"])
    if "pic" in request.files:
        minio_client.upload_pic(Config.MINIO_BUCKET, tweet_id, request.files["pic"])
    return "Tweet created", 201


def get_id(db, hash_name):
    count = "count"
    if not db.hexists(hash_name, count):
        db.hset(hash_name, count, 1)
    else:
        db.hincrby(hash_name, count)
    return db.hget(hash_name, count)
