from flask import Flask

from .config import DevConfig
from .extensions import ckeditor, db, login_manager
from .models import User
from .routes.auth import auth_bp
from .routes.main import main_bp
from .routes.posts import posts_bp


def create_app(config_class: type = DevConfig) -> Flask:
    """Application factory for the portfolio site."""

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)

    return app


@login_manager.user_loader
def load_user(user_id: str):
    """Flask-Login user loader callback."""

    try:
        return User.query.get(int(user_id))
    except (TypeError, ValueError):
        return None
