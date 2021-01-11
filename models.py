"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Table"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(20),
                        nullable=False)
    last_name = db.Column(db.String(20),
                        nullable=False)
    image_url = db.Column(db.String,
                        nullable=True,
                        default="https://bowerbird-app.s3.amazonaws.com/production/uploads/publication/image/1330/small_default_profile.png")

    def get_full_name(self):
        """Get full name"""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} - {u.first_name} {u.last_name}>"

    @classmethod
    def alphabetize_list(cls):
        """Alphabetize list based on last_name, then first_name"""

        return cls.query.order_by(cls.last_name, cls.first_name).all()

class Post(db.Model):
    """Post Table"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String,
                        nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    created_at = db.Column(db.DateTime, 
                        default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
    tagged_posts = db.relationship('PostTag', backref='post')
    tags = db.relationship('Tag',
                            secondary='post_tags',
                            backref='posts')

    def friendly_date(self):
        """Return date and time in friendly looking version"""

        now = self.created_at
        return now.strftime("%c")

    @classmethod
    def five_recent_posts(cls):
        """Return the five most recent posts"""

        return cls.query.order_by(cls.created_at.desc()).limit(5).all()

class Tag(db.Model):
    """Tag Table"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String,
                        nullable=False)

    tagged_posts = db.relationship('PostTag',
                                backref='tag')

class PostTag(db.Model):
    """PostTag Table"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                    db.ForeignKey('posts.id'),
                    primary_key=True)

    tag_id = db.Column(db.Integer,
                    db.ForeignKey('tags.id'),
                    primary_key=True)
