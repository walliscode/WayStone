from flask import Flask

 # import blueprints
from waystone import home

def create_app(test_config=None):
    app = Flask(
        __name__
    )  # create instance of Flask, passing __name__ as argument for its name

    if test_config:
        app.config.from_mapping(
            test_config
        )  # if test_config is passed, update the app's config with the test_config

   
    app.register_blueprint(home.bp)  # register the home blueprint



    return app
