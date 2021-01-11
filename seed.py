from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Ciro", last_name="Griffiths")
u2 = User(first_name="Elise", last_name="Polentes")
u3 = User(first_name="Daniel", last_name="Griffiths")
u4 = User(first_name="Faith", last_name="Griffiths")

db.session.add_all([u1, u2, u3, u4])
db.session.commit()

p1 = Post(title="First Post", content="So excited!!", user_id=1)
p2 = Post(title="Sneakerhead", content="Nike Airs", user_id=3)
p3 = Post(title="Paella party", content="Socializing!", user_id=2)
p4 = Post(title="Gardening", content="I love zinias", user_id=4)

db.session.add_all([p1, p2, p3, p4])
db.session.commit()

t1 = Tag(name="Art")
t2 = Tag(name="Gardening")
t3 = Tag(name="Food")

db.session.add_all([t1, t2, t3])
db.session.commit()

pt1 = PostTag(post_id=3, tag_id=3)
pt2 = PostTag(post_id=3, tag_id=2)

db.session.add_all([pt1, pt2])
db.session.commit()