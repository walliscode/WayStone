from flask import Blueprint

bp = Blueprint("diagrams", __name__, url_prefix="/diagrams")

from waystone.diagrams import routes