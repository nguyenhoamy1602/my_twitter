# -*- coding: utf-8 -*-

import os

#import google.oauth2.credentials
#import googleapiclient.discovery
from flask import Blueprint, redirect, request, session, url_for, jsonify

from my_twitter.utils.token import generate_token
from my_twitter.utils.user_utils import get_google_user

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.route("/", methods=["POST"])
def get_token():
    user_data = request.get_json()
    user = get_google_user(user_data)
    if user:
        return jsonify(token=generate_token(user), user=user.json())
    return jsonify(error=True), 403


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
