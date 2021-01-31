"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), 
                primary_key=True, unique=True)
 
    password = db.Column(db.Text,
                nullable=False)

    email = db.Column(db.String(50),
                nullable=False, unique=True)

    first_name = db.Column(db.String(30),
                nullable=False)
  
    last_name = db.Column(db.String(30),
                nullable=False)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

    def get_full_name(self):
        """Get full name"""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.username} - {u.first_name} {u.last_name}>"

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
    rating = db.Column(db.Integer,
                        nullable=False)
    created_at = db.Column(db.DateTime, 
                        default=datetime.datetime.utcnow)
    username = db.Column(db.String,
                        db.ForeignKey('users.username'))

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