from __future__ import annotations

from pathlib import Path
from typing import Any

from app.repositories.cv_repository import CVRepository
from app.services.pdf_service import PDFService
from app.services.render_service import RenderService


class CVService:
    """Application service for loading, saving, rendering, and exporting CV data."""

    def __init__(
        self,
        repository: CVRepository,
        render_service: RenderService,
        pdf_service: PDFService,
        output_dir: Path,
        default_theme: str = "terminal.css",
    ) -> None:
        self.repository = repository
        self.render_service = render_service
        self.pdf_service = pdf_service
        self.output_dir = output_dir
        self.default_theme = default_theme

    def load_cv(self) -> dict[str, Any]:
        return self.repository.load()

    def save_cv(self, data: dict[str, Any]) -> None:
        self.repository.save(data)

    def generate_outputs(self, data: dict[str, Any], theme_css: str | None = None) -> tuple[Path, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        html_file = self.output_dir / "cv_output.html"
        pdf_file = self.output_dir / "cv_output.pdf"

        self.render_service.render_and_save(
            data=data,
            output_file=html_file,
            theme_css=theme_css or self.default_theme,
        )
        self.pdf_service.generate_pdf(html_file, pdf_file)

        return html_file, pdf_file

    def save_and_generate(self, data: dict[str, Any], theme_css: str | None = None) -> tuple[Path, Path]:
        self.save_cv(data)
        return self.generate_outputs(data, theme_css=theme_css)

    def ensure_preview_exists(self, theme_css: str | None = None) -> tuple[Path, Path]:
        html_file = self.output_dir / "cv_output.html"
        pdf_file = self.output_dir / "cv_output.pdf"

        if html_file.exists() and pdf_file.exists():
            return html_file, pdf_file

        data = self.load_cv()
        return self.generate_outputs(data, theme_css=theme_css)