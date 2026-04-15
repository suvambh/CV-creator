from __future__ import annotations

from flask import Flask

from app.routes.editor import editor_bp
from app.routes.preview import preview_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config")

    # Keep this configurable later if you want.
    app.secret_key = "change-this-secret-key"

    app.register_blueprint(editor_bp)
    app.register_blueprint(preview_bp)

    return app