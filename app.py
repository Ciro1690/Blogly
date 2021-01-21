"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "SECRET!")
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def homepage():
    """Direct to homepage"""

    recent_posts = Post.five_recent_posts()
    return render_template("home.html", recent_posts=recent_posts)

@app.route("/users")
def list_users():
    """List users and button to add new user."""

    users = User.alphabetize_list()
    return render_template("list_users.html",users=users)

@app.route("/users/new")
def add_user():
    """Form to add new user."""
    return render_template("new_user.html")

@app.route("/users/new", methods=["POST"])
def commit_user():
    """Add user and redirect to list."""

    first = request.form['first']
    last = request.form['last']
    url = request.form['url']
    url = url if url else None

    user = User(first_name=first, last_name=last, image_url=url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def commit_edit_user(user_id):
    """Add user and redirect to list."""

    first = request.form['first']
    last = request.form['last']
    url = request.form['url']
    url = url if url else None

    user = User.query.filter_by(id=user_id).first()
    user.first_name = first
    user.last_name = last
    user.image_url = url
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edit form on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete a single user."""

    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect(f"/users")

@app.route("/users/<int:user_id>/posts/new")
def create_post(user_id):
    """Redirect to form to create new post"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def commit_post(user_id):
    """Add post to database"""

    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)

    post = Post(title=title, content=content, user_id=user.id)
    db.session.add(post)
    db.session.commit()

    tags = request.form.getlist('tag')

    for t in tags:
        tag = Tag.query.filter_by(name = t).first()
        pt = PostTag(post_id=post.id, tag_id=tag.id)
        db.session.add(pt)
        db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Detail page for a single post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Edit a single post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def commit_edit_post(post_id):
    """Edit post and redirect to user detail."""

    title = request.form['title']
    content = request.form['content']

    post = Post.query.filter_by(id=post_id).first()
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    tags = request.form.getlist('tag')

    for tag in post.tags:
        if (tag.name not in tags):
            delete = PostTag.query.filter(PostTag.post_id == post.id, PostTag.tag_id == tag.id).first()

            db.session.delete(delete)       
            db.session.commit()  

    for t in tags:
        tag = Tag.query.filter_by(name = t).first()

        if (post not in tag.posts):
            pt = PostTag(post_id=post.id, tag_id=tag.id)
            db.session.add(pt)
            db.session.commit()     

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete a single post."""

    post = Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users")    

@app.route("/tags")
def list_tags():
    """List all tags"""

    tags = Tag.query.all()
    return render_template("list_tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show info on a single tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)

@app.route("/tags/new")
def add_tag():
    """Form to add a new tag"""

    return render_template("new_tag.html")

@app.route("/tags/new", methods=["POST"])
def commit_tag():
    """Add tag and redirect to list."""

    name = request.form['name']

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Edit form for a single tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def commit_edit_tag(tag_id):
    """Edit tag and redirect to tag list."""

    name = request.form['name']

    tag = Tag.query.filter_by(id=tag_id).first()
    tag.name = name

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete")
def delete_tag(tag_id):
    """Delete a single tag."""

    tag = Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect("/tags")    