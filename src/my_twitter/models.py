from my_twitter.config import Config
from my_twitter.db import get_db


class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.follower = []
        self.following = []

    @staticmethod
    def get_username(client_id):
        return get_db().hget(Config.REDIS_USER, client_id)

    @staticmethod
    def get_user_by_id(user_id):
        db = get_db()
        return User(user_id, db.hget(Config.REDIS_USER, user_id))

    @staticmethod
    def get_user(user_id, user_name, user_pic):
        db = get_db()
        if db.hget(Config.REDIS_USER, user_id):
            return User(user_id, user_name)
        else:
            return User.create_user(user_id, user_name, user_pic)

    @staticmethod
    def create_user(client_id, username, pic):
        db = get_db()
        follower = "%s:%s" % (client_id, Config.REDIS_FOLLOWER)
        following = "%s:%s" % (client_id, Config.REDIS_FOLLOWING)

        db.hset(Config.REDIS_USER, client_id, username)

        db.hset(Config.REDIS_FOLLOWER, follower, "")
        db.hset(Config.REDIS_FOLLOWER, following, "")

        return User(client_id, username)

    @staticmethod
    def user_jsonify(user_id):
        db = get_db()
        return {"id": user_id, "name": db.hget(Config.REDIS_USER, user_id)}

    @staticmethod
    def tweet_jsonify(tweet_id):
        db = get_db()
        print("TWEET ID: " + tweet_id)
        return {
            "id": tweet_id.split(":")[0],
            "user": db.hget(Config.REDIS_USER, tweet_id.split(":")[1]),
            "name": db.hget(Config.REDIS_TWEET, tweet_id),
        }
