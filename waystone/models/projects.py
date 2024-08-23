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
    unit = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Criteria {self.name}>"


class MilestoneCriteria(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    milestone_id = db.Column(db.Integer, db.ForeignKey("milestone.id"), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey("criteria.id"), nullable=False)
    value = db.Column(db.Float, nullable=True)
    milestone = db.relationship(
        "Milestone", backref=db.backref("milestone_criteria", lazy=True)
    )
    criteria = db.relationship(
        "Criteria", backref=db.backref("milestone_criteria", lazy=True)
    )

    def __repr__(self):
        return f"<MilestoneCriteria {self.milestone_id} - {self.criteria_id}>"


class MileStoneParentChild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("milestone.id"), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey("milestone.id"), nullable=False)
    parent = db.relationship("Milestone", foreign_keys=[parent_id])
    child = db.relationship("Milestone", foreign_keys=[child_id])

    def __repr__(self):
        return f"<MilestoneParentChild {self.parent_id} - {self.child_id}>"
