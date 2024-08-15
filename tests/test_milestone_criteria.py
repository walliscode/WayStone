from waystone.extensions import db
from waystone.models import Project, Milestone, Criteria, MilestoneCriteria


def test_milestone_criteria_get(client):
    response = client.get("/project/milestone_criteria")
    assert response.status_code == 200
    assert b"milestone criteria" in response.data


def test_milestone_criteria_post(client):
    query_one = db.session.scalars(db.select(MilestoneCriteria)).all()
    assert len(query_one) == 0


    new_project = Project(name="test", description="test")
    db.session.add(new_project)
    new_milestone = Milestone(name="test", description="test", project_id=1)
    db.session.add(new_milestone)
    new_criteria = Criteria(name="test", unit="test")
    db.session.add(new_criteria)

    db.session.commit()
    response = client.post(
        "/project/milestone_criteria",
        data={"milestone_choices": 1, "criteria_choices": 1, "value": 2.0, "submit": True},
    )

    assert response.status_code == 200
    query_two = db.session.scalars(db.select(MilestoneCriteria)).all()
    assert len(query_two) == 1

    assert query_two[0].value == 2.0
    