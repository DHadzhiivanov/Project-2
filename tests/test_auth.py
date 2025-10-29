import sqlite3


def test_register_login_logout_flow(client, auth):
    # Register
    rv = auth.register(username="alice", password="wonder")
    assert rv.status_code == 302
    assert "/auth/login" in rv.headers.get("Location", "")

    # Login
    rv = auth.login(username="alice", password="wonder")
    assert rv.status_code == 302
    assert "/posts" in rv.headers.get("Location", "")

    # Logged-in user can see posts page
    rv = client.get("/posts")
    assert rv.status_code == 200

    # Logout
    rv = auth.logout()
    assert rv.status_code == 302
    # After logout, posts should redirect to login
    rv = client.get("/posts")
    assert rv.status_code == 302
    assert "/auth/login" in rv.headers.get("Location", "")


def test_register_duplicate_username_shows_flash(client, auth):
    auth.register(username="bob", password="secret")
    rv = auth.register(username="bob", password="secret")
    # Should stay on register page with a flash, not 500
    assert rv.status_code in (200, 302)
    # Follow to page to capture flash
    if rv.status_code == 302:
        rv = client.get(rv.headers["Location"], follow_redirects=True)
    assert b"already exists" in rv.data


def test_disable_requires_confirmation_and_succeeds(client, auth):
    # Create account and login
    auth.register(username="charlie", password="delta")
    auth.login(username="charlie", password="delta")

    # GET disable confirmation page
    rv = client.get("/auth/disable")
    assert rv.status_code == 200

    # Wrong password -> flash and redirect to home
    rv = client.post("/auth/disable", data={"password": "wrong"})
    assert rv.status_code == 302
    assert "/" == rv.headers.get("Location", "")
    rv = client.get("/")
    assert b"Wrong password" in rv.data

    # Correct password -> account deleted, logged out
    rv = client.post("/auth/disable", data={"password": "delta"})
    assert rv.status_code == 302
    # Should be redirected home
    assert rv.headers.get("Location", "").endswith("/")

    # Access posts should redirect to login (session cleared)
    rv = client.get("/posts")
    assert rv.status_code == 302
    assert "/auth/login" in rv.headers.get("Location", "")

    # Login should now fail since user was deleted
    rv = auth.login(username="charlie", password="delta")
    # Renders login page with error flash
    assert rv.status_code in (200, 302)
    if rv.status_code == 302:
        rv = client.get(rv.headers["Location"], follow_redirects=True)
    assert b"incorrect" in rv.data.lower()
