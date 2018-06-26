import json

import redis
from flask import Flask, request
from my_twitter.minio import My_Minio
from my_twitter.config import Config

app = Flask(__name__)
CONFIG = Config
minio_client = My_Minio(
    CONFIG.MINIO_HOST,
    minio_access_key=CONFIG.MINIO_ACCESS_KEY,
    minio_secret_key=CONFIG.MINIO_SECRET_KEY,
    secure=False,
)
db = redis.Redis(
    host=CONFIG.REDIS_URL, port=CONFIG.REDIS_PORT, db=0, decode_responses=True
)


@app.route("/tweet", methods=["POST", "GET", "PUT", "DELETE"])
def handle_create():
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
            minio_client.upload_pic(CONFIG.MINIO_BUCKET, tweet_id, request.files["pic"])
        return "Tweet created", 201

    elif request.method == "PUT":
        tweet = request.form
        if db.hget(hash_name, tweet["id"]):
            db.hset(hash_name, tweet["id"], tweet["text"])
            if "pic" in request.files:
                minio_client.upload_pic(
                    CONFIG.MINIO_BUCKET, tweet["id"], request.files["pic"]
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


def main():
    minio_client.create_bucket(CONFIG.MINIO_BUCKET)
    from . import auth

    app.register_blueprint(auth.bp)
    app.add_url_rule("/", endpoint="index")
    app.run()
