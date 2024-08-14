from flask import render_template, request


from waystone.project import bp
from waystone.extensions import db
from waystone.models import Project
from .forms import NewProjectForm, ProjectsForm


@bp.route("/", methods=["GET", "POST"])
def index():
    form = NewProjectForm()
    form2 = ProjectsForm()

    if request.method == "POST":
        if form.submit.data:
            new_project = Project(
                name=form.name.data, description=form.description.data
            )
            db.session.add(new_project)
            db.session.commit()

   
    return render_template("project/index.html", form=form, form2=form2)
    