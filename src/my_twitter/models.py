import json

from my_twitter import my_s3
from my_twitter.config import Config
from my_twitter.db import get_db


class User:
    ID = "id"
    NAME = "name"
    PROFILE_PIC = "profile_pic"
    FOLLOWER = "follower"
    FOLLOWING = "following"

    def __init__(self, user_id, name, user_email, profile_pic=""):
        self.id = user_id
        self.name = name
        self.email = user_email
        self.profile_pic = profile_pic
        self.follower = []
        self.following = []

    @staticmethod
    def get_username(user_id):
        return get_db().hget(user_id, User.NAME)

    @staticmethod
    def get_profile_pic(user_id):
        return get_db().hget(user_id, User.PROFILE_PIC)

    @staticmethod
    def get_user_by_id(user_id):
        db = get_db()
        user = User(user_id, User.get_username(user_id), User.get_profile_pic(user_id))
        user.follower = list(db.smembers(User.get_follow_key(user_id, User.FOLLOWER)))
        user.following = list(db.smembers(User.get_follow_key(user_id, User.FOLLOWING)))
        return user

    @staticmethod
    def get_follow_key(user_id, follow_type):
        return user_id + ":" + follow_type

    def follow(self, user_id):
        get_db().sadd(User.get_follow_key(self.id, User.FOLLOWING), user_id)
        get_db().sadd(user_id, User.FOLLOWER, self.id)

    @staticmethod
    def get_user(client_id, user_name, user_pic):
        db = get_db()
        user_id = db.hget(Config.REDIS_USER, client_id)
        if not user_id:
            user_id = User.create_user(client_id, user_name, user_pic)
        # return db.hget(Config.REDIS_USER, client_id)
        # return user_id
        return User.get_user_by_id(user_id)

    @staticmethod
    def get_google_user(user_data):
        return User.get_user(
            user_data["googleId"], user_data["name"], user_data["imageUrl"]
        )

    @staticmethod
    def create_user(client_id, username, pic):
        db = get_db()
        follower = "%s:%s" % (client_id, Config.REDIS_FOLLOWER)
        following = "%s:%s" % (client_id, Config.REDIS_FOLLOWING)
        user_id = "%s:%s" % (Config.REDIS_USER, get_id(db, Config.REDIS_USER))
        User.save_user_to_db(user_id, username, pic)
        db.hset(Config.REDIS_USER, client_id, user_id)
        return user_id

    @staticmethod
    def save_user_to_db(user_id, username, pic):
        db = get_db()
        db.hset(user_id, User.NAME, username)
        db.hset(user_id, User.PROFILE_PIC, pic)

    @staticmethod
    def user_jsonify(user):
        db = get_db()
        return {
            User.ID: user.id,
            User.NAME: user.name,
            User.PROFILE_PIC: user.profile_pic,
            User.FOLLOWING: user.following,
            User.FOLLOWER: user.follower,
        }


class Tweet:
    def __init__(self, tweet_id, text, author, has_photo, date):
        self.id = tweet_id
        self.text = text
        self.author = author
        self.has_photo = has_photo
        self.date = date


def get_id(db, hash_name):
    count = "count"
    if not db.hexists(hash_name, count):
        db.hset(hash_name, count, 1)
    else:
        db.hincrby(hash_name, count)
    return db.hget(hash_name, count)
