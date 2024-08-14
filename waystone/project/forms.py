from flask_wtf import FlaskForm
from waystone.extensions import db
from waystone.models import Project

from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField


class NewProjectForm(FlaskForm):
    name = StringField("Project Name")
    description = StringField("Project Description")
    submit = SubmitField("Create Project")


class ProjectsForm(FlaskForm):
    project_choices = QuerySelectField(
        "Select Project",
        query_factory=lambda: db.session.scalars(db.select(Project)).all(),
        allow_blank=False,
        get_label=lambda project: "{} - {}".format(project.name, project.description)  # Example of including another field
    )
