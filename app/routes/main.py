from flask import Blueprint, render_template
from flask_login import current_user

from app.extensions import db
from app.models import BlogPost, Comment, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def homepage():
    """Render the homepage with all blog posts."""

    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@main_bp.route("/about", methods=["GET"])
def about():
    """Render the about page."""

    return render_template("about.html", current_user=current_user)


@main_bp.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""

    return "OK", 200
