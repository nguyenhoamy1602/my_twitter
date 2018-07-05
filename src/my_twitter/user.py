import json

import flask


from my_twitter.config import Config
from my_twitter.db import get_db
from my_twitter.models import User
from my_twitter.utils.token import requires_auth
from my_twitter.utils.user_utils import get_user_by_id

bp = flask.Blueprint("user", __name__, url_prefix="/api")


# @login_required
@bp.route("/user", methods=["GET"])
def get_user():
    db = get_db()
    user_list = []
    for i in db.smembers(User.LIST):
        user_list.append(get_user_by_id(i).json())
    return flask.jsonify(user_list), 200


# @bp.route("/follow", method=["POST"])
# @requires_auth
# def follow():
#     current_user = g.current_user
#     user_to_follow = request.
