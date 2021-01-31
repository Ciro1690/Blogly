"""Everyone's a critic application."""

from flask import Flask, request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from forms import RegisterForm, LoginForm, PostForm
from sqlalchemy.exc import IntegrityError
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
def home():
    """Direct to Home Page"""

    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username already taken")
            return render_template("register.html", form=form)

        session['username'] = new_user.username
        flash("Created new account", "success")
        return redirect('/')

    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome {user.first_name}", "success")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)
    
@app.route("/recent")
def recent():
    """Direct to Recent Posts"""
    recent_posts = Post.five_recent_posts()
    return render_template("recent.html", recent_posts=recent_posts)

@app.route("/users/<username>")
def user_info(username):
    user = User.query.get_or_404(username)
    return render_template("user_info.html", user=user)

@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash("Please log in to view this page", "danger")
        return redirect('/login')
    if session['username'] == username:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted", "success")
        return redirect("/logout")
    flash("You don't have permission", "danger")
    return redirect("/")

@app.route("/users")
def list_users():
    """List users and button to add new user."""

    users = User.alphabetize_list()
    return render_template("list_users.html",users=users)

@app.route("/users/<username>/edit", methods=["POST"])
def commit_edit_user(username):
    """Add user and redirect to list."""

    first = request.form['first']
    last = request.form['last']
    email = request.form['email']

    user = User.query.filter_by(username=username).first()
    user.first_name = first
    user.last_name = last
    user.email = email

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users")

@app.route("/users/<username>/edit")
def edit_user(username):
    """Edit form on a single user."""

    user = User.query.get_or_404(username)
    return render_template("edit_user.html", user=user)

@app.route("/users/<username>/posts/new", methods=['GET', 'POST'])
def create_post(username):
    """Create new post"""
    if 'username' not in session:
        flash("Please login first", "danger")
        return redirect('/')
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        rating = form.rating.data

        user = User.query.get_or_404(username)
        post = Post(title=title, content=content, rating=rating, username=username)
        db.session.add(post)
        db.session.commit()

        tags = request.form.getlist('tag')

        for t in tags:
            tag = Tag.query.filter_by(name = t).first()
            pt = PostTag(post_id=post.id, tag_id=tag.id)
            db.session.add(pt)
            db.session.commit()

        flash('Post added', "success")
        return redirect(f"/users/{username}")
    tags = Tag.query.all()
    return render_template("new_post.html", tags=tags, form=form)

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

    return redirect(f"/users/{post.username}")

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete a single post."""

    post = Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users")    

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show info on a single tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)

@app.route("/logout")
def logout():
    session.pop('username')
    flash('You are now logged out', "success")
    return redirect('/')