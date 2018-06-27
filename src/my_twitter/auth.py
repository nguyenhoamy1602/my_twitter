# -*- coding: utf-8 -*-

import functools
import os

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)

from my_twitter.config import Config
from my_twitter.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = os.path.join(os.getcwd(), "src/client_secret.json")

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/plus.me",
    "email",
]

# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See http://pocoo.org/docs/0.12/quickstart/#sessions.
# app.secret_key = 'REPLACE ME - this value is here as a placeholder.'


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.authorize"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    if session.get("credentials"):
        g.user = get_user()[0]
    else:
        g.user = None


def get_username(client_id):
    return get_db().hget(Config.REDIS_USER, client_id)


def get_user():
    if "credentials" not in session:
        return redirect("authorize")

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    plus = googleapiclient.discovery.build("plus", "v1", credentials=credentials)
    user = plus.people().get(userId="me").execute()
    return user["id"], user["displayName"], user["image"]["url"]


def create_user(client_id, username, pic):
    db = get_db()
    follower = "%s:%s" % (client_id, Config.REDIS_FOLLOWER)
    following = "%s:%s" % (client_id, Config.REDIS_FOLLOWING)

    db.hset(Config.REDIS_USER, client_id, username)

    db.hset(Config.REDIS_FOLLOWER, follower, "")
    db.hset(Config.REDIS_FOLLOWER, following, "")


@bp.route("/authorize")
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    flow.redirect_uri = url_for("auth.oauth2callback", _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # Store the state so the callback can verify the auth server response.
    session["state"] = state

    return redirect(authorization_url)


@bp.route("/oauth2callback")
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session["state"]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = url_for("auth.oauth2callback", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    user_id, username, pic = get_user()
    if get_username(user_id):
        g.user = username
    else:
        create_user(user_id, username, pic)
    return redirect(url_for("user.get_user"))


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))


# @bp.route("/revoke")
# def revoke():
#     if "credentials" not in session:
#         return (
#             'You need to <a href="/authorize">authorize</a> before '
#             + "testing the code to revoke credentials."
#         )
#
#     credentials = google.oauth2.credentials.Credentials(**session["credentials"])
#
#     revoke = requests.post(
#         "https://accounts.google.com/o/oauth2/revoke",
#         params={"token": credentials.token},
#         headers={"content-type": "application/x-www-form-urlencoded"},
#     )
#
#     status_code = getattr(revoke, "status_code")
#     if status_code == 200:
#         return "Credentials successfully revoked."
#     else:
#         return "An error occurred."
#
#
# @bp.route("/clear")
# def clear_credentials():
#     if "credentials" in session:
#         del session["credentials"]
#     return "Credentials have been cleared.<br><br>"


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
