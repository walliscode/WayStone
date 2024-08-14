from waystone.extensions import db


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # def __repr__(self):
    #     return f"<Project {self.name}>"


class Milestone(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    project = db.relationship("Project", backref=db.backref("milestones", lazy=True))

    def __repr__(self):
        return f"<Milestone {self.name}>"


class Criteria(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(255), nullable=False)

    milestone_id = db.Column(db.Integer, db.ForeignKey("milestone.id"), nullable=False)
    milestone = db.relationship("Milestone", backref=db.backref("criteria", lazy=True))

    def __repr__(self):
        return f"<Criteria {self.name}>"
