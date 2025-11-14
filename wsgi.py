"""WSGI entrypoint for the portfolio site using the application factory."""

from app import create_app
from app.config import ProdConfig


app = create_app(ProdConfig)
