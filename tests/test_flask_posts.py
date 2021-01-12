from unittest import TestCase

from app import app
from models import db, User, Tag, Post, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample post."""

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        Post.query.delete()

        post = Post(title="First", content="Post", user_id=1)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>First</h1>', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Second", "content": "Post"}
            resp = client.post("/users/1/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Second", html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.get("posts/1/delete", follow_redirects=True)
            post = client.get("posts/1")

            self.assertEqual(post.status_code, 404)
