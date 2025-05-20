import pytest

from myapp import app


@pytest.fixture
def client():
    return app.test_client()


class TestUser:

    def test_succesful_fetching_a_user(self, client):
        response = client.get("api/v1/users/1")

        assert response.status_code == 200
        assert response.json == {
            "id": 1,
            "firstname": "foo",
            "lastname": "bar",
        }

    def test_failed_fetching_a_user(self, client):
        response = client.get("api/v1/users/999")

        assert response.status_code == 404
        assert response.json["error"] == "user not found"

    def test_successful_updating_a_user(self, client):
        # add a user for the update & delete test
        response = client.post(
            "api/v1/users",
            data={
                "firstname": "not updated",
                "lastname": "user",
            },
        )

        assert response.status_code == 201
        assert response.json["msg"] == "successfully inserted new user"

        response = client.put(
            "api/v1/users/2",
            json={
                "firstname": "updated",
                "lastname": "user"
            }
        )

        assert response.status_code == 201
        assert response.json["msg"] == "successfully updated user"

        # check if user is really updated
        response = client.get("api/v1/users/2")

        assert response.status_code == 200
        assert response.json == {
            "id": 2,
            "firstname": "updated",
            "lastname": "user",
        }

    def test_failed_updating_a_user(self, client):
        response = client.put(
            "api/v1/users/999",
            json={
                "firstname": "updated",
                "lastname": "user"
            }
        )

        assert response.status_code == 404
        assert response.json["error"] == "user not found"
    
    def test_successful_deleting_a_user(self, client):
        response = client.delete("api/v1/users/2")

        assert response.status_code == 201
        assert response.json["msg"] == "successfully deleted user"

        # check if user is really deleted
        response = client.get("api/v1/users/2")

        assert response.status_code == 404
        assert response.json["error"] == "user not found"

    def test_failed_deleting_a_user(self, client):
        response = client.delete("api/v1/users/999")

        assert response.status_code == 404
        assert response.json["error"] == "user not found"