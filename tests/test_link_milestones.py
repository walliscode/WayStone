
def test_link_milestone_get(client):

    response = client.get("/project/link_milestones")

    assert response.status_code == 200
    assert b"Linking Milestones" in response.data