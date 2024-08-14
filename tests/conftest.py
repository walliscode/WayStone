import pytest

from waystone import create_app
from waystone.extensions import db


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "dev",
        }
    )  # create instance of Flask, passing config dict with TESTING set to True

    with app.app_context():
        db.create_all()  # create all tables in the database
        yield app
        db.drop_all


@pytest.fixture
def client(app):
    return (
        app.test_client()
    )  # create a test client for the app, this mimics requests withou running a live server
