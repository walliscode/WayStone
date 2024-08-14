from flask import Blueprint

bp = Blueprint("home", __name__, url_prefix="/")    # create a Blueprint instance with the name "home" and the url_prefix "/"

from . import routes  # import the routes module from the current package