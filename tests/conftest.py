import os
import tempfile
import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite")
    try:
        app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": db_path,
        })

        with app.app_context():
            init_db()

        yield app
    finally:
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def register(self, username="test", password="test"):
        return self._client.post(
            "/auth/register", data={"username": username, "password": password}
        )

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
