import functools
from hashlib import sha256
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} already exists."
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Username or password is incorrect.'
        elif not check_password_hash(user['password'], password):
            error = 'Username or password is incorrect.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.posts'))

        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/disable', methods=('GET',))
@login_required
def disable_page():
    """Show a confirmation page with a form to disable the account."""
    return render_template('auth/disable.html')


@bp.route('/disable', methods=('POST',))
@login_required
def disable():
    confirmation = request.form.get('password', '')
    error = None

    if not check_password_hash(g.user['password'], confirmation):
        error = 'Wrong password.'
        flash(error)
        return redirect(url_for('blog.home'))

    db = get_db()
    try:
        db.execute('DELETE FROM post WHERE author_id = ?', (g.user['id'],))
        db.execute('DELETE FROM user WHERE id = ?', (g.user['id'],))
        db.commit()
    except db.IntegrityError:
        error = 'Unable to remove account due to related data.'
        flash(error)
        return redirect(url_for('blog.home'))

    session.clear()
    flash('Account disabled successfully.')
    return redirect(url_for('blog.home'))
