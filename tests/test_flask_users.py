from unittest import TestCase

from app import app
from models import db, User, Tag, Post, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vlpbjjer:kTGa7Pew6zSWQco2gAJ67p1s0Kx_LeuL@mahmud.db.elephantsql.com/vlpbjjer'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first": "Second", "last": "User", "url": 'www.google.com'}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Second User</h1>", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test', html)

# class PostViewsTestCase(TestCase):
#     """Tests for views for Posts."""

#     def setUp(self):
#         """Add sample post."""

#         user = User(first_name="Test", last_name="User")
#         db.session.add(user)
#         db.session.commit()

#         Post.query.delete()

#         post = Post(title="First", content="Post", user_id=1)
#         db.session.add(post)
#         db.session.commit()

#         self.user_id = user.id

#     def tearDown(self):
#         """Clean up any fouled transaction."""

#         db.session.rollback()


#     def test_show_post(self):
#         with app.test_client() as client:
#             resp = client.get(f"/posts/{self.post_id}")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn('<h1>New</h1>', html)

    # def test_add_post(self):
    #     with app.test_client() as client:
    #         d = {"title": "Second", "content": "Post"}
    #         resp = client.post("/users/1/posts/new", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h1>Second</h1>", html)

    # def test_delete_user(self):
    #     with app.test_client() as client:
    #         resp = client.get("users/3/delete", follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn('Test', html)