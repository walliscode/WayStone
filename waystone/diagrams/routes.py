from waystone.diagrams import bp
from waystone.extensions import db
from waystone.models import Project, Milestone, MileStoneParentChild
from flask import render_template
import graphviz


@bp.route("/", methods=["GET"])
def index():
    # get data from database
    # Get all projects from the database
    projects = db.session.scalars(db.select(Project)).all()

    # Create a new diagram
    main_diagram = graphviz.Digraph(
        graph_attr={"rankdir": "LR", "splines": "ortho"},
        node_attr={"shape": "rectangle", "style": "rounded, filled", "color": "red"},
    )

    # add clusters for each project
    for project in projects:
        # get project name
        project_name = project.name
        # get milestones for the project
        milestones = db.session.scalars(
            db.select(Milestone).filter(Milestone.project_id == project.id)
        ).all()

        with main_diagram.subgraph(name="cluster_{}".format(project_name)) as c:
            c.attr(
                label=project_name,
                style="filled, rounded",
                color="lightgrey",
            )

            for milestone in milestones:
                # loop throug milestones and add them to the diagram as nodes
                c.node(str(milestone.id), milestone.name)

                # add edges
                milestone_links = db.session.scalars(
                    db.select(MileStoneParentChild).filter(
                        MileStoneParentChild.parent_id == milestone.id
                    )
                ).all()
                for link in milestone_links:
                    main_diagram.edge(str(link.parent_id), str(link.child_id))

    # turn into image
    main_diagram.render(
        "waystone/static/diagrams/main_diagram", format="svg", cleanup=True
    )

    return render_template("diagrams/index.html", projects=projects)
