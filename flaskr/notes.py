from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.encryption import generate_key, encrypt_text, decrypt_text

bp = Blueprint('blog', __name__)


@bp.route('/posts')
@login_required
def posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, p.title, p.body, p.created, p.author_id '
        'FROM post p '
        'WHERE p.author_id = ? '
        'ORDER BY p.created DESC ',
        (g.user['id'],)
    ).fetchall()
    one_time_key = session.pop('one_time_key', None)
    return render_template('notes.html', posts=posts, one_time_key=one_time_key)


@bp.route('/write', methods=('GET', 'POST'))
@login_required
def write():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body = request.form.get('message', '')
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Message is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            key = generate_key()
            body_enc = encrypt_text(body, key)
            db.execute(
                'INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)',
                (title, body_enc, g.user['id'])
            )
            db.commit()
            session['one_time_key'] = key
            return redirect(url_for('blog.posts'))

    return render_template('write.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        if 'decrypt' in request.form:
            key = request.form.get('key', '')
            try:
                body_plain = decrypt_text(post['body'], key)
            except Exception:
                flash('Wrong key.')
                return render_template('update.html', post=post, decrypted=False)
            return render_template('update.html', post=post, decrypted=True, key=key, body_plain=body_plain)
        elif 'save' in request.form:
            title = request.form.get('title', '').strip()
            body_plain = request.form.get('body', '')
            key = request.form.get('key', '')
            if not title:
                flash('Title is required.')
                return render_template('update.html', post=post, decrypted=True, key=key, body_plain=body_plain)
            db = get_db()
            body_enc = encrypt_text(body_plain, key)
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body_enc, id)
            )
            db.commit()
            return redirect(url_for('blog.posts'))
    return render_template('update.html', post=post, decrypted=False)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.posts'))


@bp.route('/')
def home():
    return render_template('home.html')
