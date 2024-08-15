from flask_wtf import FlaskForm
from waystone.extensions import db
from waystone.models import Project, Criteria, Milestone

from wtforms import StringField, SubmitField
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
        get_label=lambda project: "{} - {}".format(
            project.name, project.description
        )
    )


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
            milestone.name, milestone.description, milestone.project_id, milestone.project.name
        )
    )

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
