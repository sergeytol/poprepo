from unittest import mock
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from github.GithubException import UnknownObjectException
from github.Repository import Repository

from app.main import app

client = TestClient(app)
headers = {"GitHub-Access-Token": "test"}


def test_root():
    response = client.get("/")
    assert response.status_code == 404


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_popularity():
    """Test /repo/{owner}/{repo}/popularity endpoint"""

    response = client.get("/repo/test//popularity")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

    response = client.post("/repo/test/test/popularity")
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}

    response = client.get("/repo/sergeytol/poprepo/popularity")
    assert response.status_code == 400
    assert response.json() == {"detail": "Access token is required"}

    response = client.get(
        "/repo/sergeytol/poprepo/popularity", headers={"GitHub-Access-Token": "test"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid access token"}

    # repository not found or is private
    with mock.patch("app.main.get_repo") as mocked:
        mocked.side_effect = UnknownObjectException(
            mock.Mock(status=404), "not found", headers={}
        )
        response = client.get("/repo/sergeytol/poprepo/popularity", headers=headers)
        assert response.status_code == 404
        assert response.json() == {"detail": "Repository not found or is private"}

    # not popular
    mocked = MagicMock()
    repo = Repository(
        requester=MagicMock(),
        headers=MagicMock(),
        completed=MagicMock(),
        attributes={"stargazers_count": 499, "forks": 0},
    )
    mocked_inst = mocked.return_value
    mocked_inst = repo
    with mock.patch("app.main.get_repo", return_value=mocked_inst):
        response = client.get("/repo/sergeytol/poprepo/popularity", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"is_popular": False}

    # popular
    repo = Repository(
        requester=MagicMock(),
        headers=MagicMock(),
        completed=MagicMock(),
        attributes={"stargazers_count": 0, "forks": 250},
    )
    mocked_inst = mocked.return_value
    mocked_inst = repo
    with mock.patch("app.main.get_repo", return_value=mocked_inst):
        response = client.get("/repo/sergeytol/poprepo/popularity", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"is_popular": True}
