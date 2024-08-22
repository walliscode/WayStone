def test_diagrams_home (client):
    response = client.get("/diagrams/")

    assert response.status_code == 200
    