from waystone.extensions import db
from waystone.models import Project, Milestone


def test_milestone_addition_get(client):
    
        response = client.get("/project/milestone")
    
        assert response.status_code == 200
        assert b"milestone" in response.data

def test_milestone_addition_post(client):
        
        query_one = db.session.scalars(db.select(Milestone)).all()
        assert len(query_one) == 0

        new_project = Project(name="test", description="test")
        db.session.add(new_project)
        db.session.commit()

        response = client.post("/project/milestone", data={"name": "test", "description": "test",
                                                           "link_project": 1,
                                                           "submit": True})
        
        assert response.status_code == 200
        query_two = db.session.scalars(db.select(Milestone)).all()

        assert len(query_two) == 1
