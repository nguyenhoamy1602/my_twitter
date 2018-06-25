from my_twitter import cli


def test_api():
    assert cli.api() == "interns"


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
