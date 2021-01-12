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

class TagViewsTestCase(TestCase):
    """Tests for views for Tags."""

    def setUp(self):
        """Add sample tag."""

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        post = Post(title="First", content="Post", user_id=1)
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="Tag1")
        db.session.add(tag)
        db.session.commit()        

        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tag1', html)

    def test_add_tag(self):
        with app.test_client() as client:
            d = {"name": "Tag2"}
            resp = client.post(f"/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Tag2", html)

    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.get("tags/1/delete", follow_redirects=True)
            tag = client.get("tags/1")

            self.assertEqual(tag.status_code, 404)
