import json

import flask


from my_twitter.config import Config
from my_twitter.db import get_db
from my_twitter.models import User
from my_twitter.utils.token import requires_auth

bp = flask.Blueprint("user", __name__, url_prefix="/api")


@bp.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html")


@bp.route("/home", methods=["GET"])
def home():
    return print_index_table()


# @login_required
@bp.route("/user", methods=["GET"])
def get_user():
    db = get_db()
    user_list = []
    for i in db.hgetall(Config.REDIS_USER):
        user_list.append(User.user_jsonify(i))
    return flask.jsonify(user_list), 200


# @bp.route("/follow", method=["POST"])
# @requires_auth
# def follow():
#     db = get_db()
#     user_id =


def print_index_table():
    return (
        "<table>"
        + '<tr><td><a href="/tweet">See Tweet</a></td>'
        + "<td>Submit an API request and see a formatted JSON response. "
        + "    Go through the authorization flow if there are no stored "
        + "    credentials for the user.</td></tr>"
        + '<tr><td><a href="/authorize">Test the auth flow directly</a></td>'
        + "<td>Go directly to the authorization flow. If there are stored "
        + "    credentials, you still might not be prompted to reauthorize "
        + "    the application.</td></tr>"
        + '<tr><td><a href="/revoke">Revoke current credentials</a></td>'
        + "<td>Revoke the access token associated with the current user "
        + "    session. After revoking credentials, if you go to the test "
        + "    page, you should see an <code>invalid_grant</code> error."
        + "</td></tr>"
        + '<tr><td><a href="/clear">Clear Flask session credentials</a></td>'
        + "<td>Clear the access token currently stored in the user session. "
        + '    After clearing the token, if you <a href="/test">test the '
        + "    API request</a> again, you should go back to the auth flow."
        + "</td></tr></table>"
    )
