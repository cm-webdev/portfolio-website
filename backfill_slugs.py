import os

from app import create_app
from app.config import DevConfig, ProdConfig
from app.extensions import db
from app.models import BlogPost


def backfill_slugs():
    """Populate slug for any BlogPost that doesn't have one."""

    count = 0
    posts = BlogPost.query.filter(
        (BlogPost.slug.is_(None)) | (BlogPost.slug == "")
    ).all()
    for post in posts:
        post.slug = BlogPost._slugify(post.title)
        count += 1
    db.session.commit()
    print(f"Updated {count} posts with generated slugs.")


if __name__ == "__main__":
    app = create_app(DevConfig)
    with app.app_context():
        backfill_slugs()
