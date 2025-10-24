from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from cryptography.exceptions import InvalidTag

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.encryption import encrypt_message, decrypt_message

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
    return render_template('posts.html', posts=posts)


@bp.route('/write', methods=('GET', 'POST'))
@login_required
def write():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body_plain = request.form.get('message', '')
        enc_password = request.form.get('enc_password', '')
        error = None

        if not title:
            error = 'Title is required.'
        elif not body_plain:
            error = 'Message is required.'
        elif not enc_password:
            error = 'Encryption password is required to store the note.'

        if error is not None:
            flash(error)
        else:
            # encrypt plaintext with provided password and store ciphertext
            try:
                body_encrypted = encrypt_message(body_plain, enc_password)
            except Exception as e:
                flash('Encryption failed.')
                return render_template('write.html', title=title, message=body_plain)

            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body_encrypted, g.user['id'])
            )
            db.commit()
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

    # default: no decrypted body
    decrypted_body = None

    if request.method == 'POST':
        action = request.form.get('action', 'save')
        if action == 'decrypt':
            # attempt to decrypt stored ciphertext using provided password
            enc_password = request.form.get('enc_password', '')
            if not enc_password:
                flash('Encryption password is required to decrypt.')
            else:
                try:
                    decrypted_body = decrypt_message(
                        post['body'], enc_password)
                except InvalidTag:
                    flash('Wrong password or corrupted data.')
                except Exception:
                    flash('Decryption failed.')
            # render template with decrypted_body (if successful it will be shown in textarea)
            return render_template('update.html', post=post, decrypted_body=decrypted_body)

        elif action == 'save':
            # saving: encrypt the provided plaintext body with supplied password
            title = request.form.get('title', '').strip()
            body_plain = request.form.get('body', '')
            enc_password = request.form.get('enc_password', '')
            error = None

            if not title:
                error = 'Title is required.'
            elif not enc_password:
                error = 'Encryption password is required to save the note.'

            if error is not None:
                flash(error)
            else:
                try:
                    body_encrypted = encrypt_message(body_plain, enc_password)
                except Exception:
                    flash('Encryption failed.')
                    return render_template('update.html', post=post, decrypted_body=body_plain)

                db = get_db()
                db.execute(
                    'UPDATE post SET title = ?, body = ? WHERE id = ?',
                    (title, body_encrypted, id)
                )
                db.commit()
                return redirect(url_for('blog.posts'))

    # GET: render page showing encrypted body by default
    return render_template('update.html', post=post, decrypted_body=decrypted_body)


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
