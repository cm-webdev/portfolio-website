from datetime import date

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from app.extensions import db
from app.forms import CreatePostForm, LoginForm, admin_only
from app.models import BlogPost, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["GET", "POST"])
def login():
    """Login view mirroring the existing implementation in main.py."""

    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("auth.login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("auth.login"))
        else:
            login_user(user)
            return redirect(url_for("main.homepage"))

    return render_template("login.html", form=form, current_user=current_user)


@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    """Logout endpoint mirroring the existing implementation."""

    logout_user()
    return redirect(url_for("main.homepage"))


@auth_bp.route("/admin", methods=["GET"])
def admin_dashboard():
    """Placeholder for admin dashboard."""

    return "Admin dashboard placeholder"


@auth_bp.route("/admin/posts", methods=["GET", "POST"])
@admin_only
def admin_posts():
    """Admin post creation mirroring the existing add_new_post route."""

    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            summary=form.summary.data or None,
            category=form.category.data or None,
            thumbnail_url=form.thumbnail_url.data or None,
            github_url=form.github_url.data or None,
            live_url=form.live_url.data or None,
            is_featured=bool(form.is_featured.data),
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("main.homepage"))
    return render_template("make-post.html", form=form, current_user=current_user)


@auth_bp.route("/admin/posts/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    """Edit an existing blog post, including metadata fields."""

    post = BlogPost.query.get_or_404(post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body,
        summary=post.summary,
        category=post.category,
        thumbnail_url=post.thumbnail_url,
        github_url=post.github_url,
        live_url=post.live_url,
        is_featured=post.is_featured_safe,
    )

    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        post.summary = form.summary.data or None
        post.category = form.category.data or None
        post.thumbnail_url = form.thumbnail_url.data or None
        post.github_url = form.github_url.data or None
        post.live_url = form.live_url.data or None
        post.is_featured = bool(form.is_featured.data)

        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("posts.post_detail", slug=post.slug or post.id))

    return render_template("make-post.html", form=form, is_edit=True, post=post)
