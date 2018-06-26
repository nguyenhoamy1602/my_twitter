from flask import Flask, request
import redis
import json

REDIS_URL = "localhost"

app = Flask(__name__)
app.debug = True

db = redis.Redis(host=REDIS_URL, port=6379, db=0, decode_responses=True)


@app.route("/tweet", methods=["POST", "GET", "PUT", "DELETE"])
def handle_create():
    hash_name = "Tweet"
    count = "count"

    if request.method == "POST":
        new_tweet = request.get_json()["text"]
        if not db.hexists(hash_name, count):
            db.hset(hash_name, count, 1)
        else:
            db.hincrby(hash_name, count)
        tweet_id = "#%s:%s" % (db.hget(hash_name, count), "user")
        db.hset(hash_name, tweet_id, new_tweet)
        return "Tweet created", 201

    elif request.method == "PUT":
        tweet = request.get_json()
        if db.hget(hash_name, tweet["id"]):
            db.hset(hash_name, tweet["id"], tweet["text"])
            return json.dumps({tweet["id"]: db.hget(hash_name, tweet["id"])}), 201
        else:
            return "Tweet not found", 404

    elif request.method == "DELETE":
        tweet_id = request.get_json()["id"]
        if db.hdel(hash_name, tweet_id):
            return tweet_id + " deleted", 201
        return "Tweet not found", 404

    else:
        # return json.dumps({"tweets": db.hgetall(hash_name)})
        return json.dumps({hash_name: db.hgetall(hash_name)})


def main():
    app.run()
