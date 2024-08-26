from flask import render_template, request, session, flash, redirect, url_for
from sqlalchemy import or_


from waystone.project import bp
from waystone.extensions import db
from waystone.models import (
    Project,
    Criteria,
    Milestone,
    MilestoneCriteria,
    MileStoneParentChild,
)
from .forms import (
    NewProjectForm,
    CurrentProjectsForm,
    NewMilestoneForm,
    CurrentMilestonesForm,
    NewCriteriaForm,
    CurrentCriteriaForm,
    NewMilestoneCriteriaForm,
    LinkMileStonesForm,
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

        # delete project, we need to cascade delete the milestones and milestone criteria
        if form2.delete_project.data:

            project = form2.project_choices.data

            milestones = db.session.scalars(
                db.select(Milestone).filter(Milestone.project_id == project.id)
            ).all()  # get all milestones for the project

            for milestone in milestones:
                print(milestone)
                # delete all milestone criteria for the milestone
                db.session.execute(
                    db.delete(MilestoneCriteria).filter(
                        MilestoneCriteria.milestone_id == milestone.id
                    )
                )
                # delete all parent child relationships for the milestone if it is a parent or child
                db.session.execute(
                    db.delete(MileStoneParentChild).filter(
                        or_(
                            MileStoneParentChild.parent_id == milestone.id,
                            MileStoneParentChild.child_id == milestone.id,
                        )
                    )
                )
                # delete the milestone
                db.session.delete(milestone)

            # delete the project
            db.session.delete(project)
            db.session.commit()

            message = f"Project {project.name} deleted successfully"
            flash(message)
            # session.clear

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
        
        if form2.delete_milestone.data:
            milestone = form2.milestone_choices.data
            db.session.execute(
                db.delete(MilestoneCriteria).filter(
                    MilestoneCriteria.milestone_id == milestone.id
                )   
            )
            db.session.execute(
                db.delete(MileStoneParentChild).filter(
                    or_(
                        MileStoneParentChild.parent_id == milestone.id,
                        MileStoneParentChild.child_id == milestone.id,
                    )
                )
            )
            db.session.delete(milestone)
            db.session.commit()
            message = f"Milestone {milestone.name} deleted successfully"
            flash(message)

            return redirect(url_for("project.index"))
    
    

    return render_template("project/milestone.html", form=form, form2=form2)


@bp.route("/link_milestones", methods=["GET", "POST"])
def link_milestones():
    form = LinkMileStonesForm()

    if request.method == "POST":
        if form.select_child_project.data:
            session["child_project"] = {}
            session["child_project"]["id"] = form.project_choices.data.id
            session["child_project"]["name"] = form.project_choices.data.name

        if form.select_child_milestone.data:
            session["child_milestone"] = {}
            session["child_milestone"]["id"] = form.milestone_choices.data.id
            session["child_milestone"]["name"] = form.milestone_choices.data.name

        if form.select_parent_project.data:
            session["parent_project"] = {}
            session["parent_project"]["id"] = form.project_choices.data.id
            session["parent_project"]["name"] = form.project_choices.data.name

        if form.select_parent_milestone.data:
            session["parent_milestone"] = {}
            session["parent_milestone"]["id"] = form.milestone_choices.data.id
            session["parent_milestone"]["name"] = form.milestone_choices.data.name

        if form.link_milestones.data:
            new_milestone_link = MileStoneParentChild(
                parent_id=session["parent_milestone"]["id"],
                child_id=session["child_milestone"]["id"],
            )
            db.session.add(new_milestone_link)
            db.session.commit()
            session.clear()

        if form.reset.data:
            session.clear()

    if "child_project" in session:
        # update the query factory for milestones by filtering by the child project
        form.milestone_choices.query_factory = lambda: db.session.scalars(
            db.select(Milestone).filter(
                Milestone.project_id == session["child_project"]["id"]
            )
        ).all()

        if "parent_project" in session:
            form.milestone_choices.query_factory = lambda: db.session.scalars(
                db.select(Milestone).filter(
                    Milestone.project_id == session["parent_project"]["id"],
                    Milestone.id != session["child_milestone"]["id"],
                )
            ).all()

    return render_template("project/link_milestones.html", form=form)


@bp.route("/milestone_criteria", methods=["GET", "POST"])
def milestone_criteria():
    form = NewMilestoneCriteriaForm()

    if request.method == "POST":
        if form.select_project.data:
            form.milestone_choices.query_factory = lambda: db.session.scalars(
                db.select(Milestone).filter(
                    Milestone.project_id == form.project_choices.data.id
                )
            ).all()
            session["project"] = {}
            session["project"]["id"] = form.project_choices.data.id
            session["project"]["name"] = form.project_choices.data.name
            session["project"]["description"] = form.project_choices.data.description

        if form.submit.data:
            new_milestone_criteria = MilestoneCriteria(
                milestone_id=form.milestone_choices.data.id,
                criteria_id=form.criteria_choices.data.id,
                value=form.value.data,
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
