from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user

from app.extensions import db
from app.forms import CommentForm
from app.models import BlogPost, Comment

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/posts/<slug>", methods=["GET", "POST"])
def post_detail(slug):
    """Post detail view matching the existing logic in main.py."""

    try:
        post_id = int(slug)
    except (TypeError, ValueError):
        abort(404)

    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("auth.login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post,
        )
        db.session.add(new_comment)
        db.session.commit()

    return render_template(
        "post.html", post=requested_post, current_user=current_user, form=comment_form
    )


@posts_bp.route("/category/<slug>", methods=["GET"])
def posts_by_category(slug):
    """Placeholder for posts filtered by category."""

    return f"Posts in category placeholder for: {slug}"
