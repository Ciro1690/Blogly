"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/users")
def list_users():
    """List users and button to add new user."""

    users = User.alphabetize_list()
    return render_template("list.html",users=users)

@app.route("/users/new")
def add_user():
    """Form to add new user."""
    return render_template("new.html")

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
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edit form on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete a single user."""

    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect(f"/users")
