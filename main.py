import json
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
DATA_FILE = BASE_DIR / "data.json"

#THEME = "classic-tech.css"   # change to "modern-tech.css" when needed
THEME = "terminal.css"

def load_data(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_html(data: dict, theme_css: str) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("cv.html")
    return template.render(**data, theme_css=theme_css)


def save_html(content: str, output_file: Path) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)


def save_pdf(html_file: Path, pdf_file: Path) -> None:
    subprocess.run(
        ["/usr/bin/weasyprint", str(html_file), str(pdf_file)],
        check=True,
        cwd=BASE_DIR
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    data = load_data(DATA_FILE)
    rendered_html = render_html(data, THEME)

    html_output_file = OUTPUT_DIR / "cv_output.html"
    pdf_output_file = OUTPUT_DIR / "cv_output.pdf"

    save_html(rendered_html, html_output_file)
    save_pdf(html_output_file, pdf_output_file)

    print(f"Theme used:      {THEME}")
    print(f"HTML generated:  {html_output_file}")
    print(f"PDF generated:   {pdf_output_file}")


if __name__ == "__main__":
    main()