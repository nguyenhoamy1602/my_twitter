import datetime
import time

from flask import Blueprint, g, request, jsonify

from my_twitter import my_s3
from my_twitter.config import Config
from my_twitter.db import get_db
from my_twitter.models import User
from my_twitter.utils.token import requires_auth

bp = Blueprint("tweet", __name__, url_prefix="/api/tweet")

ID = "id"
TEXT = "text"
IMAGE = "image"
HAS_IMAGE = "has_image"
USER = "user"
USER_IMAGE = "userImage"
DATE = "date"
TRUE = "1"
FALSE = "0"
NOT_FOUND = "Tweet not found"
DATE_TIME_FORMAT = "%d-%m-%Y %H:%M"


@bp.route("/", methods=["DELETE"])
@requires_auth
def delete_tweet():
    db = get_db()
    tweet_id = request.args[ID]
    if db.zrem(Config.REDIS_TWEET, tweet_id):
        if db.hget(tweet_id, HAS_IMAGE) == TRUE:
            my_s3.delete(tweet_id)
        db.delete(tweet_id)
        return jsonify(message=tweet_id + " deleted"), 200
    return jsonify(error=NOT_FOUND), 404


@bp.route("/", methods=["GET", "OPTIONS"])
# @requires_auth
def get_tweet():
    db = get_db()
    tweet_list = []
    for i in db.zrevrangebyscore(Config.REDIS_TWEET, time.time(), 0):
        tweet_list.append(tweet_jsonify(i))
    return jsonify(tweet_list)


@bp.route("/", methods=["POST"])
@requires_auth
def post_tweet():
    tweet = request.form

    tweet_id = get_tweet_id()
    has_image = save_pic_to_s3(request, tweet_id)
    save_tweet_to_db(tweet_id, tweet, has_image)

    return jsonify(tweet_jsonify(tweet_id)), 200


@bp.route("/", methods=["PUT"])
@requires_auth
def update_tweet():
    db = get_db()
    tweet = request.form
    tweet_id = tweet[ID]
    if db.hgetall(tweet_id):
        db.hset(tweet_id, TEXT, tweet[TEXT])
        return jsonify(tweet_jsonify(tweet_id)), 200
    return jsonify(error=NOT_FOUND), 404


def get_id(db, key):
    key = key + ":count"
    if not db.exists(key):
        db.set(key, 1)
    else:
        db.incr(key)
    return db.get(key)


def get_tweet_id():
    db = get_db()
    return "%s:%s" % (Config.REDIS_TWEET, get_id(db, Config.REDIS_TWEET))


def save_pic_to_s3(request, tweet_id):
    if IMAGE in request.files:
        my_s3.upload(request.files[IMAGE], tweet_id)
        return TRUE
    return FALSE


def save_tweet_to_db(tweet_id, tweet, has_image):
    db = get_db()
    date = str(time.time())
    db.hset(tweet_id, TEXT, tweet[TEXT])
    db.hset(tweet_id, USER, g.current_user["name"])
    db.hset(tweet_id, USER_IMAGE, User.get_profile_pic(g.current_user["id"]))
    db.hset(tweet_id, HAS_IMAGE, has_image)
    db.hset(tweet_id, DATE, date)

    db.zadd(Config.REDIS_TWEET, tweet_id, date)


def tweet_jsonify(i):
    db = get_db()
    image_url = my_s3.get_presigned_url(i) if db.hget(i, HAS_IMAGE) == TRUE else None
    date = get_date(i)

    return {
        ID: i,
        USER: db.hget(i, USER),
        USER_IMAGE: db.hget(i, USER_IMAGE),
        TEXT: db.hget(i, TEXT),
        IMAGE: image_url,
        DATE: date,
    }


def get_date(tweet):
    date = get_db().hget(tweet, DATE)
    date = time.strftime(DATE_TIME_FORMAT, time.localtime(float(date)))
    return date
