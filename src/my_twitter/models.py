import json

from my_twitter import my_s3
from my_twitter.config import Config
from my_twitter.db import get_db
from my_twitter.utils import user_utils


class User:
    ID = "id"
    NAME = "name"
    PROFILE_PIC = "profile_pic"
    FOLLOWER = "follower"
    FOLLOWING = "following"
    CLIENT = "UserClientMap"
    LIST = "UserList"
    REDIS_KEY = "User:"

    def __init__(self, user_id, name, profile_pic):
        self.id = user_id
        self.name = name
        self.profile_pic = profile_pic
        self.follower = []
        self.following = []

    def follow(self, user_id):
        get_db().sadd(user_utils.get_follow_key(self.id, User.FOLLOWING), user_id)
        get_db().sadd(user_id, User.FOLLOWER, self.id)

    def json(self):
        print("SELF: " + self.profile_pic)
        return {
            User.ID: self.id,
            User.NAME: self.name,
            User.PROFILE_PIC: self.profile_pic,
            User.FOLLOWING: self.following,
            User.FOLLOWER: self.follower,
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
