from flask import Blueprint, jsonify

from my_twitter.auth import login_required
from my_twitter.config import Config
from my_twitter.db import get_db

bp = Blueprint("user", __name__)


@bp.route("/", methods=["GET"])
def home():
    return print_index_table()


@login_required
def get_user():
    db = get_db()
    return jsonify({Config.REDIS_USER: db.hgetall(Config.REDIS_USER)})


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
