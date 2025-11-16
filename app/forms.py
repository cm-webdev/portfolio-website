"""WTForms and admin utilities for the portfolio application."""

from functools import wraps

from flask import abort
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional, URL


class CreatePostForm(FlaskForm):
    """WTForm for creating or editing blog posts."""

    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = TextAreaField("Blog Content", validators=[DataRequired()])
    summary = TextAreaField("Summary", validators=[Optional(), Length(max=1000)])
    category = SelectField(
        "Category",
        choices=[
            ("webapp", "Web app"),
            ("gui", "GUI app"),
            ("console", "Console / terminal"),
            ("general", "General"),
        ],
        default="webapp",
    )
    thumbnail_url = StringField(
        "Thumbnail URL", validators=[Optional(), URL(), Length(max=500)]
    )
    github_url = StringField(
        "GitHub URL", validators=[Optional(), URL(), Length(max=500)]
    )
    live_url = StringField("Live URL", validators=[Optional(), URL(), Length(max=500)])
    is_featured = BooleanField("Featured project")
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    """Form for registering a new user."""

    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    """Form for logging in an existing user."""

    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):
    """Form for adding a comment to a post."""

    comment_text = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


def admin_only(f):
    """Decorator ensuring only the admin user (id == 1) can access a route."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function
