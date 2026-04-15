from __future__ import annotations

from flask import current_app

from app.repositories.cv_repository import CVRepository
from app.services.cv_service import CVService
from app.services.pdf_service import PDFService
from app.services.render_service import RenderService


def get_cv_service() -> CVService:
    repository = CVRepository(current_app.config["DATA_FILE"])
    render_service = RenderService(
        current_app.config["TEMPLATES_DIR"],
        default_theme=current_app.config["DEFAULT_THEME"],
    )
    pdf_service = PDFService(
        current_app.config["BASE_DIR"],
        weasyprint_bin=current_app.config["WEASYPRINT_BIN"],
    )

    return CVService(
        repository=repository,
        render_service=render_service,
        pdf_service=pdf_service,
        output_dir=current_app.config["OUTPUT_DIR"],
        default_theme=current_app.config["DEFAULT_THEME"],
    )