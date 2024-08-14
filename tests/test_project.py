from waystone.extensions import db
from waystone.models import Project

def test_project_index(client):

    response = client.get("/project/")
    assert response.status_code == 200


def test_project_post_project(client):

    query_one = db.session.scalars(db.select(Project))
    assert len(list(query_one)) == 0
    
    response = client.post("/project/", data={"name": "Test Project", "description": "Test Description", "submit": True})
    client.post("/project/", data={"name": "Test Project 2", "description": "Test Description 2", "submit": True})
    assert response.status_code == 200

    query_two = db.session.scalars(db.select(Project)).all()


    assert len(query_two) == 2
    assert query_two[0].name == "Test Project"
    assert query_two[0].description == "Test Description"
    assert query_two[0].id == 1

    assert query_two[1].name == "Test Project 2"
    assert query_two[1].description == "Test Description 2"
    assert query_two[1].id == 2

 
    
