from waystone.extensions import db
from waystone.models import Criteria


def test_criteria_addition_get(client):

    response = client.get("/project/criteria")

    assert response.status_code == 200
    assert b"criteria" in response.data


def test_criteria_addition_post(client):

    query_one = db.session.scalars(db.select(Criteria)).all()
    assert len(query_one) == 0

    response = client.post(
        "/project/criteria",
        data={"name": "Test Criteria", "unit": "Test Unit", "submit": True},
    )
    assert response.status_code == 200

    query_two = db.session.scalars(db.select(Criteria)).all()
    assert len(query_two) == 1
