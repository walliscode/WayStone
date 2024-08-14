from flask import Flask
from waystone.extensions import db
from waystone import models

# import blueprints
from waystone import home, project


def create_app(test_config=None):
    app = Flask(
        __name__, instance_relative_config=True
    )  # create instance of Flask, passing __name__ as argument for its name
    if test_config is None:
        app.config.from_pyfile("instance_config.py")
    else:

        app.config.from_mapping(
            test_config
        )  # if test_config is passed, update the app's config with the test_config

    app.register_blueprint(home.bp)  # register the home blueprint
    app.register_blueprint(project.bp)  # register the project blueprint

    # register the database
    db.init_app(app)

    return app
