from flask import Blueprint, jsonify

from my_twitter.config import Config
from my_twitter.db import get_db

bp = Blueprint("user", __name__)


@bp.route("/", methods=["GET"])
def get_user():
    db = get_db()
    return jsonify({Config.REDIS_USER: db.hgetall(Config.REDIS_USER)})
