import pytest


def login_as(client, username, password):
    return client.post("/auth/login", data={"username": username, "password": password})


def create_user(client, username="u1", password="pw1"):
    client.post("/auth/register",
                data={"username": username, "password": password})


def test_posts_requires_login(client):
    rv = client.get("/posts")
    assert rv.status_code == 302
    assert "/auth/login" in rv.headers.get("Location", "")


def test_write_validation_and_create(client):
    create_user(client, "author", "pass")
    login_as(client, "author", "pass")

    # Missing fields -> flash and re-render
    rv = client.post("/write", data={"title": "", "message": ""})
    assert rv.status_code == 200
    assert b"Title is required" in rv.data or b"Message is required" in rv.data

    # Create valid note
    rv = client.post("/write", data={"title": "T1", "message": "Body1"})
    assert rv.status_code == 302 and "/posts" in rv.headers.get("Location", "")

    # Listed on /posts
    rv = client.get("/posts")
    assert b"T1" in rv.data


def test_update_and_delete_by_author(client):
    create_user(client, "author2", "pass2")
    login_as(client, "author2", "pass2")

    # Create post
    client.post("/write", data={"title": "Old", "message": "Old body"})

    # Find post id by visiting posts page and scraping link
    rv = client.get("/posts")
    assert rv.status_code == 200
    # crude parse for '/<id>/update'
    import re
    m = re.search(rb"href=\"/([0-9]+)/update\"", rv.data)
    assert m, "Expected edit link in posts list"
    post_id = int(m.group(1))

    # Update
    rv = client.post(f"/{post_id}/update",
                     data={"title": "New", "body": "New body"})
    assert rv.status_code == 302 and "/posts" in rv.headers.get("Location", "")
    rv = client.get("/posts")
    assert b"New" in rv.data
    assert b"Old" not in rv.data

    # Delete
    rv = client.post(f"/{post_id}/delete")
    assert rv.status_code == 302 and "/posts" in rv.headers.get("Location", "")
    rv = client.get("/posts")
    assert b"<h1>New</h1>" not in rv.data


def test_only_author_sees_and_can_modify_own_posts(client):
    # user1 creates a post
    create_user(client, "u1", "p1")
    login_as(client, "u1", "p1")
    client.post("/write", data={"title": "u1-title", "message": "b"})
    rv = client.get("/posts")
    import re
    m = re.search(rb"href=\"/([0-9]+)/update\"", rv.data)
    assert m
    post_id = int(m.group(1))

    # user2 logs in and shouldn't see u1's edit link and cannot access update/delete
    client.get("/auth/logout")
    create_user(client, "u2", "p2")
    login_as(client, "u2", "p2")

    # user2's posts should be empty, so u1-title not present
    rv = client.get("/posts")
    assert b"u1-title" not in rv.data

    # Accessing u1's post update/delete should be forbidden
    rv = client.get(f"/{post_id}/update")
    assert rv.status_code == 403
    rv = client.post(f"/{post_id}/delete")
    assert rv.status_code == 403
