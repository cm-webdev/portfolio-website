from flask import Blueprint, render_template
from flask_login import current_user

from app.extensions import db
from app.models import BlogPost, Comment, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def homepage():
    """Render the homepage with featured and other projects."""

    featured_webapps = (
        BlogPost.query.filter_by(category="webapp", is_featured=True)
        .order_by(BlogPost.id.desc())
        .limit(3)
        .all()
    )
    featured_ids = [post.id for post in featured_webapps]
    other_projects = (
        BlogPost.query.filter(~BlogPost.id.in_(featured_ids))
        .order_by(BlogPost.id.desc())
        .all()
    )
    return render_template(
        "index.html",
        featured_webapps=featured_webapps,
        other_projects=other_projects,
        current_user=current_user,
    )


@main_bp.route("/about", methods=["GET"])
def about():
    """Render the about page."""

    return render_template("about.html", current_user=current_user)


@main_bp.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""

    return "OK", 200


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Render the contact page."""

    return render_template("contact.html", current_user=current_user)
