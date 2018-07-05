from my_twitter.db import get_db
from my_twitter.models import User


def get_google_user(user):
    user_id = get_user_by_client_id(user["googleId"])
    if not user_id:
        user_id = create_user_id(user["email"])
        create_user(user_id, user["name"], user["imageUrl"])
        add_to_list(user_id)
        map_client_user(user["googleId"], user_id)
    return get_user_by_id(user_id)


def create_user(user_id, username, pic):
    db = get_db()
    db.hset(user_id, User.NAME, username)
    db.hset(user_id, User.PROFILE_PIC, pic)
    return user_id


def get_user_by_id(user_id):
    db = get_db()
    user = User(user_id, get_username(user_id), get_profile_pic(user_id))
    print("PROFILE PIC: " + get_profile_pic(user_id))
    user.follower = list(db.smembers(get_follow_key(user_id, User.FOLLOWER)))
    user.following = list(db.smembers(get_follow_key(user_id, User.FOLLOWING)))
    return user


def add_to_list(user_id):
    get_db().sadd(User.LIST, user_id)


def get_user_by_client_id(client_id):
    return get_db().hget(User.CLIENT, client_id)


def get_username(user_id):
    return get_db().hget(user_id, User.NAME)


def get_profile_pic(user_id):
    return get_db().hget(user_id, User.PROFILE_PIC)


def map_client_user(client_id, user_id):
    get_db().hset(User.CLIENT, client_id, user_id)


def create_user_id(user_email):
    return User.REDIS_KEY + user_email


def get_follow_key(user_id, follow_type):
    return user_id + ":" + follow_type
