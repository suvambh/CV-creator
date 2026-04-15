from __future__ import annotations

from flask import Blueprint, current_app, redirect, send_from_directory, url_for

from app.dependencies import get_cv_service


preview_bp = Blueprint("preview", __name__)


@preview_bp.get("/preview")
def preview():
    cv_service = get_cv_service()
    cv_service.ensure_preview_exists()
    return redirect(url_for("preview.output_file", filename="cv_output.html"))


@preview_bp.get("/pdf")
def pdf():
    cv_service = get_cv_service()
    cv_service.ensure_preview_exists()
    return redirect(url_for("preview.output_file", filename="cv_output.pdf"))


@preview_bp.get("/output/<path:filename>")
def output_file(filename: str):
    return send_from_directory(current_app.config["OUTPUT_DIR"], filename)