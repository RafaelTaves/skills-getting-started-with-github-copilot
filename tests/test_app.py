from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"],
        }
    }


def test_unregister_participant_removes_from_activity():
    client = TestClient(app_module.app)
    email = "student@mergington.edu"
    app_module.activities["Chess Club"]["participants"].append(email)

    response = client.delete(f"/activities/Chess Club/participants/{quote(email)}")

    assert response.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]
