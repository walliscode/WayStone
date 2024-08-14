import pytest

from waystone import create_app


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
        }
    )  # create instance of Flask, passing config dict with TESTING set to True

    yield app


@pytest.fixture
def client(app):
    return app.test_client()  # create a test client for the app, this mimics requests withou running a live server
