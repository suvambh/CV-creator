from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class PDFService:
    """Generate PDF files from HTML using WeasyPrint."""

    def __init__(self, base_dir: Path, weasyprint_bin: str = "/usr/bin/weasyprint") -> None:
        self.base_dir = base_dir
        self.weasyprint_bin = weasyprint_bin

    def _resolve_weasyprint_bin(self) -> str:
        """Return a valid WeasyPrint executable path."""
        if Path(self.weasyprint_bin).exists():
            return self.weasyprint_bin

        discovered = shutil.which("weasyprint")
        if discovered:
            return discovered

        raise FileNotFoundError(
            "WeasyPrint executable not found. "
            "Install WeasyPrint or configure the correct executable path."
        )

    def generate_pdf(self, html_file: Path, pdf_file: Path) -> Path:
        """Generate a PDF from an HTML file."""
        if not html_file.exists():
            raise FileNotFoundError(f"HTML source file not found: {html_file}")

        pdf_file.parent.mkdir(parents=True, exist_ok=True)
        weasyprint_bin = self._resolve_weasyprint_bin()

        subprocess.run(
            [weasyprint_bin, str(html_file), str(pdf_file)],
            check=True,
            cwd=self.base_dir,
        )
        return pdf_file