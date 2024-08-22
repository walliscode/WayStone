from waystone.diagrams import bp
from waystone.extensions import db
from waystone.models import Project

from flask import render_template
import graphviz

@bp.route("/", methods=["GET"])
def index():
    projects = db.session.scalars(db.select(Project.name)).all()

    main_diagram = graphviz.Digraph()

    for project in projects:
        main_diagram.node(project)
    
    main_diagram.render("waystone/static/diagrams/main_diagram", format="png", cleanup=True)

    return render_template("diagrams/index.html", projects=projects)