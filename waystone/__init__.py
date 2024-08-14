from flask import Flask


def create_app(test_config=None):
    app = Flask(
        __name__
    )  # create instance of Flask, passing __name__ as argument for its name

    if test_config:
        app.config.from_mapping(
            test_config
        )  # if test_config is passed, update the app's config with the test_config

    @app.route("/hello")  # create a route for the app using the route() decorator
    def hello():
        return "Hello, This Crazy World!"

    return app
