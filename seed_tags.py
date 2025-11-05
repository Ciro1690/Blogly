from app import app
from models import db, Tag

# Define the genres from your base.html
genre_tags = [
    "Movies",
    "Books",
    "TV Shows",
    "Music",
    "Video Games"
]

with app.app_context():
    for name in genre_tags:
        # Check if the tag already exists to avoid duplicates
        if not Tag.query.filter_by(name=name).first():
            tag = Tag(name=name)
            db.session.add(tag)
    db.session.commit()

    print("✅ Genre tags seeded successfully!")