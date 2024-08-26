from flask_wtf import FlaskForm
from waystone.extensions import db
from waystone.models import Project, Criteria, Milestone

from wtforms import StringField, SubmitField, DecimalField
from wtforms_sqlalchemy.fields import QuerySelectField


class NewProjectForm(FlaskForm):
    name = StringField("Project Name")
    description = StringField("Project Description")
    submit = SubmitField("Create Project")


class CurrentProjectsForm(FlaskForm):
    project_choices = QuerySelectField(
        "Select Project",
        query_factory=lambda: db.session.scalars(db.select(Project)).all(),
        allow_blank=False,
        get_label=lambda project: "{} - {}".format(project.name, project.description),
    )

    delete_project = SubmitField("Delete Project")


class NewMilestoneForm(FlaskForm):

    name = StringField("Milestone Name")
    description = StringField("Milestone Description")
    link_project = QuerySelectField(
        "Select Project",
        query_factory=lambda: db.session.scalars(db.select(Project)).all(),
        allow_blank=False,
        get_label=lambda project: "{} - {}".format(project.name, project.description),
    )
    submit = SubmitField("Add Milestone")


class CurrentMilestonesForm(FlaskForm):
    milestone_choices = QuerySelectField(
        "Select Milestone",
        query_factory=lambda: db.session.scalars(db.select(Milestone)).all(),
        allow_blank=False,
        get_label=lambda milestone: "{} - {} for project {}. {}".format(
            milestone.name,
            milestone.description,
            milestone.project_id,
            milestone.project.name,
        ),
    )

    delete_milestone = SubmitField("Delete Milestone")


class NewCriteriaForm(FlaskForm):
    name = StringField("Criteria Name")
    unit = StringField("Unit")
    submit = SubmitField("Add Criteria")


class CurrentCriteriaForm(FlaskForm):
    criteria_choices = QuerySelectField(
        "Select Criteria",
        query_factory=lambda: db.session.scalars(db.select(Criteria)).all(),
        allow_blank=False,
        get_label=lambda criteria: "{} - {}".format(criteria.name, criteria.unit),
    )


class NewMilestoneCriteriaForm(FlaskForm):
    project_choices = QuerySelectField(
        "Select Project",
        query_factory=lambda: db.session.scalars(db.select(Project)).all(),
        allow_blank=False,
        get_label=lambda project: "{} - {}".format(project.name, project.description),
    )
    select_project = SubmitField("Select Project")

    milestone_choices = QuerySelectField(
        "Select Milestone",
        query_factory=lambda: db.session.scalars(db.select(Milestone)).all(),
        allow_blank=False,
        get_label=lambda milestone: "{} - {}".format(
            milestone.name, milestone.description
        ),
    )

    criteria_choices = QuerySelectField(
        "Select Criteria",
        query_factory=lambda: db.session.scalars(db.select(Criteria)).all(),
        allow_blank=False,
        get_label=lambda criteria: "{} - {}".format(criteria.name, criteria.unit),
    )
    value = DecimalField("Value")
    submit = SubmitField("Add Criteria to Milestone")


class LinkMileStonesForm(FlaskForm):
    project_choices = QuerySelectField(
        "Select Project",
        query_factory=lambda: db.session.scalars(db.select(Project)).all(),
        allow_blank=False,
        get_label=lambda project: "{}".format(project.name),
    )
    select_child_project = SubmitField("Select Project")
    select_parent_project = SubmitField("Select Project")

    milestone_choices = QuerySelectField(
        "Select Milestone",
        query_factory=lambda: db.session.scalars(db.select(Milestone)).all(),
        allow_blank=False,
        get_label=lambda milestone: "{}".format(milestone.name),
    )

    select_child_milestone = SubmitField("Select Milestone")
    select_parent_milestone = SubmitField("Select Milestone")

    link_milestones = SubmitField("Link Milestones")

    reset = SubmitField("Reset")
