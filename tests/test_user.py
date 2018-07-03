import pytest

from my_twitter.db import get_db
from my_twitter.models import User


@pytest.fixture(autouse=True)
def client():
    from flask import Flask

    app = Flask(__name__)
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


def test_db():
    db = get_db()
    db.set("Test", "Test")
    assert db.get("Test") == "Test"
    db.flushall()


def test_create_user():
    db = get_db()
    user_id = User.create_user(123, "TEST_USER", "pic.jpg")
    assert db.hget(user_id, User.NAME) == "TEST_USER"
    db.flushall()


def test_get_user():
    db = get_db()
    user = User.get_user(123, "TEST_USER", "pic.jpg")
    # assert user.name == "TEST_USER"
    assert user.profile_pic == "pic.jpg"
    db.flushall()
