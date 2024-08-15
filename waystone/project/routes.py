from flask import render_template, request


from waystone.project import bp
from waystone.extensions import db
from waystone.models import Project, Criteria, Milestone
from .forms import (
    NewProjectForm,
    CurrentProjectsForm,
    NewMilestoneForm,
    CurrentMilestonesForm,
    NewCriteriaForm,
    CurrentCriteriaForm,
)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = NewProjectForm()
    form2 = CurrentProjectsForm()

    if request.method == "POST":
        if form.submit.data:
            new_project = Project(
                name=form.name.data, description=form.description.data
            )
            db.session.add(new_project)
            db.session.commit()

    return render_template("project/index.html", form=form, form2=form2)

@bp.route("/milestone", methods=["GET", "POST"])
def milestone():
    form = NewMilestoneForm()
    form2 = CurrentMilestonesForm()

    if request.method == "POST":
        if form.submit.data:
            new_milestone = Milestone(
                name=form.name.data,
                description=form.description.data,
                project_id=form.link_project.data.id,
            )
            db.session.add(new_milestone)
            db.session.commit()

   
  

    return render_template("project/milestone.html", form=form, form2=form2)


@bp.route("/criteria", methods=["GET", "POST"])
def criteria():
    form = NewCriteriaForm()
    form2 = CurrentCriteriaForm()

    if request.method == "POST":
        if form.submit.data:
            new_criteria = Criteria(name=form.name.data, unit=form.unit.data)
            db.session.add(new_criteria)
            db.session.commit()

    return render_template("project/criteria.html", form=form, form2=form2)
