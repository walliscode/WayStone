from flask import Blueprint

bp = Blueprint("project", __name__, url_prefix="/project")

from waystone.project import routes
