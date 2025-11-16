from datetime import date

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.forms import CreatePostForm, LoginForm, RegisterForm, admin_only
from app.models import BlogPost, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["GET", "POST"])
def login():
    """Login view mirroring the existing implementation in main.py."""

    form = LoginForm()
    is_valid = form.validate_on_submit()
    print("DEBUG admin_posts: is_valid =", is_valid, "errors =", form.errors)
    if is_valid:
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


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user account."""

    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))

    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash(
                "You’ve already signed up with that email. Please log in instead.",
                "warning",
            )
            return redirect(url_for("auth.login"))

        hashed_password = generate_password_hash(
            form.password.data, method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Account created.", "success")
        return redirect(url_for("main.homepage"))

    return render_template("register.html", form=form)


@auth_bp.route("/auth/logout", methods=["GET", "POST"])
def logout():
    """Logout endpoint mirroring the existing implementation."""

    logout_user()
    return redirect(url_for("main.homepage"))


@auth_bp.route("/admin", methods=["GET"])
@admin_only
def admin_dashboard():
    """Simple admin dashboard listing all posts."""

    posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
    return render_template(
        "admin/dashboard.html", posts=posts, current_user=current_user
    )


@auth_bp.route("/admin/posts", methods=["GET", "POST"])
@login_required
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
    form = CreatePostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.img_url = form.img_url.data
        post.summary = form.summary.data or None
        post.category = form.category.data or None
        post.thumbnail_url = form.thumbnail_url.data or None
        post.github_url = form.github_url.data or None
        post.live_url = form.live_url.data or None
        post.is_featured = bool(form.is_featured.data)

        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("auth.admin_dashboard"))

    return render_template(
        "edit-post.html", form=form, current_user=current_user, is_edit=True, post=post
    )


@auth_bp.route("/admin/posts/<int:post_id>/delete")
@login_required
@admin_only
def delete_post(post_id):
    """Delete a blog post."""

    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("auth.admin_dashboard"))
