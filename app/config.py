import os


class BaseConfig:
    """Base configuration shared across environments."""

    SECRET_KEY = os.environ.get("FLASK_KEY") or "dev-secret-change-me"
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    """Configuration for local development."""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "sqlite:///posts.db")


class ProdConfig(BaseConfig):
    """Configuration for production deployments."""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
