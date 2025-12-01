import functools
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import boto3
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


def upload_image_to_s3(file_storage):
    """Upload an image to S3 and return its public URL, or None if no file."""
    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)
    key = f"personal-blog/{uuid.uuid4()}_{filename}"

    s3 = boto3.client(
        "s3",
        region_name=current_app.config["AWS_REGION"],
    )
    bucket = current_app.config["S3_BUCKET_NAME"]

    s3.upload_fileobj(
        file_storage,
        bucket,
        key,
        ExtraArgs={
            "ContentType": file_storage.content_type,
           
        },
    )

    return f"https://{bucket}.s3.amazonaws.com/{key}"

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, image_url'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        file = request.files.get('image')
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            image_url = upload_image_to_s3(file)
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, image_url)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], image_url)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, image_url'
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
        title = request.form['title']
        body = request.form['body']
        file = request.files.get('image')
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            image_url = post['image_url']
            new_image_url = upload_image_to_s3(file)
            if new_image_url is not None:
                image_url = new_image_url

            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, image_url = ?'
                ' WHERE id = ?',
                (title, body, image_url, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
