from flask import render_template, request, session


from waystone.project import bp
from waystone.extensions import db
from waystone.models import Project, Criteria, Milestone, MilestoneCriteria
from .forms import (
    NewProjectForm,
    CurrentProjectsForm,
    NewMilestoneForm,
    CurrentMilestonesForm,
    NewCriteriaForm,
    CurrentCriteriaForm,
    NewMilestoneCriteriaForm
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


@bp.route("/milestone_criteria", methods=["GET", "POST"])
def milestone_criteria():
    form = NewMilestoneCriteriaForm()
    
    if request.method == "POST":
        if form.select_project.data:
            form.milestone_choices.query_factory = lambda: db.session.scalars(db.select(Milestone).filter(Milestone.project_id == form.project_choices.data.id)).all()
            session["project"] = {}
            session["project"]["id"] = form.project_choices.data.id
            session["project"]["name"] = form.project_choices.data.name
            session["project"]["description"] = form.project_choices.data.description
        
        if form.submit.data:
            new_milestone_criteria = MilestoneCriteria(
                milestone_id=form.milestone_choices.data.id,
                criteria_id=form.criteria_choices.data.id,
                value = form.value.data
            )
            db.session.add(new_milestone_criteria)
            db.session.commit()

            session.clear()
        
       
    return render_template("project/milestone_criteria.html", form=form)


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
