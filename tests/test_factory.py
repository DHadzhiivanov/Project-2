from flaskr import create_app


def test_config():
    app = create_app(
        {"TESTING": True, "SECRET_KEY": "x", "DATABASE": ":memory:"})
    assert app.config["TESTING"] is True


def test_index_route_registered(client):
    # root should be reachable (either via 'index' or blog.home)
    rv = client.get("/")
    assert rv.status_code in (200, 302)
