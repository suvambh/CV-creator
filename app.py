import json
import subprocess
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
DATA_FILE = BASE_DIR / "data.json"

DEFAULT_THEME = "style.css"

app = Flask(__name__)
app.secret_key = "change-this-secret-key"


def load_data() -> dict[str, Any]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def render_cv_html(data: dict[str, Any], theme_css: str = DEFAULT_THEME) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("cv.html")
    return template.render(**data, theme_css=theme_css)


def write_html_and_pdf(data: dict[str, Any], theme_css: str = DEFAULT_THEME) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    html_output_file = OUTPUT_DIR / "cv_output.html"
    pdf_output_file = OUTPUT_DIR / "cv_output.pdf"

    rendered_html = render_cv_html(data, theme_css)

    with open(html_output_file, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    subprocess.run(
        ["/usr/bin/weasyprint", str(html_output_file), str(pdf_output_file)],
        check=True,
        cwd=BASE_DIR,
    )


def split_lines(text: str) -> list[str]:
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_skills(raw_text: str) -> dict[str, list[str]]:
    """
    Expects lines like:
    Langages: Python, SQL, Bash
    Cloud & DevOps: AWS, Terraform, EKS
    """
    result: dict[str, list[str]] = {}
    for line in split_lines(raw_text):
        if ":" not in line:
            continue
        category, values = line.split(":", 1)
        category = category.strip()
        items = [item.strip() for item in values.split(",") if item.strip()]
        if category and items:
            result[category] = items
    return result


def collect_entries(prefix: str) -> list[dict[str, Any]]:
    """
    Collects repeated form fields like:
    experience_role[]
    experience_company[]
    ...
    """
    roles = request.form.getlist(f"{prefix}_role[]")
    companies = request.form.getlist(f"{prefix}_company[]")
    durations = request.form.getlist(f"{prefix}_duration[]")
    locations = request.form.getlist(f"{prefix}_location[]")
    techs = request.form.getlist(f"{prefix}_tech[]")
    details_list = request.form.getlist(f"{prefix}_details[]")

    entries: list[dict[str, Any]] = []
    max_len = max(
        [
            len(roles),
            len(companies),
            len(durations),
            len(locations),
            len(techs),
            len(details_list),
        ],
        default=0,
    )

    for i in range(max_len):
        role = roles[i].strip() if i < len(roles) else ""
        company = companies[i].strip() if i < len(companies) else ""
        duration = durations[i].strip() if i < len(durations) else ""
        location = locations[i].strip() if i < len(locations) else ""
        tech = techs[i].strip() if i < len(techs) else ""
        details_raw = details_list[i] if i < len(details_list) else ""

        if not any([role, company, duration, location, tech, details_raw.strip()]):
            continue

        entry: dict[str, Any] = {}
        if role:
            entry["role"] = role
        if company:
            entry["company"] = company
        if duration:
            entry["duration"] = duration
        if location:
            entry["location"] = location
        if tech:
            entry["tech"] = tech

        details = split_lines(details_raw)
        if details:
            entry["details"] = details

        entries.append(entry)

    return entries


def collect_projects() -> list[dict[str, Any]]:
    names = request.form.getlist("project_name[]")
    techs = request.form.getlist("project_tech[]")
    details_list = request.form.getlist("project_details[]")

    projects: list[dict[str, Any]] = []
    max_len = max([len(names), len(techs), len(details_list)], default=0)

    for i in range(max_len):
        name = names[i].strip() if i < len(names) else ""
        tech = techs[i].strip() if i < len(techs) else ""
        details_raw = details_list[i] if i < len(details_list) else ""

        if not any([name, tech, details_raw.strip()]):
            continue

        project: dict[str, Any] = {}
        if name:
            project["name"] = name
        if tech:
            project["tech"] = tech

        details = split_lines(details_raw)
        if details:
            project["details"] = details

        projects.append(project)

    return projects


def collect_education() -> list[dict[str, Any]]:
    degrees = request.form.getlist("education_degree[]")
    institutions = request.form.getlist("education_institution[]")
    years = request.form.getlist("education_year[]")

    education: list[dict[str, Any]] = []
    max_len = max([len(degrees), len(institutions), len(years)], default=0)

    for i in range(max_len):
        degree = degrees[i].strip() if i < len(degrees) else ""
        institution = institutions[i].strip() if i < len(institutions) else ""
        year = years[i].strip() if i < len(years) else ""

        if not any([degree, institution, year]):
            continue

        entry: dict[str, Any] = {}
        if degree:
            entry["degree"] = degree
        if institution:
            entry["institution"] = institution
        if year:
            entry["year"] = year

        education.append(entry)

    return education


def collect_certifications() -> list[dict[str, Any]]:
    names = request.form.getlist("cert_name[]")
    issuers = request.form.getlist("cert_issuer[]")
    years = request.form.getlist("cert_year[]")

    certifications: list[dict[str, Any]] = []
    max_len = max([len(names), len(issuers), len(years)], default=0)

    for i in range(max_len):
        name = names[i].strip() if i < len(names) else ""
        issuer = issuers[i].strip() if i < len(issuers) else ""
        year = years[i].strip() if i < len(years) else ""

        if not any([name, issuer, year]):
            continue

        cert: dict[str, Any] = {}
        if name:
            cert["name"] = name
        if issuer:
            cert["issuer"] = issuer
        if year:
            cert["year"] = year

        certifications.append(cert)

    return certifications


def build_data_from_form() -> dict[str, Any]:
    data: dict[str, Any] = {}

    for field in ["name", "title", "photo", "email", "phone", "location", "linkedin", "github", "summary"]:
        value = request.form.get(field, "").strip()
        if value:
            data[field] = value

    skills_raw = request.form.get("skills_text", "").strip()
    skills = parse_skills(skills_raw)
    if skills:
        data["skills"] = skills

    experience = collect_entries("experience")
    if experience:
        data["experience"] = experience

    projects = collect_projects()
    if projects:
        data["projects"] = projects

    education = collect_education()
    if education:
        data["education"] = education

    certifications = collect_certifications()
    if certifications:
        data["certifications"] = certifications

    return data


def skills_to_text(skills: dict[str, list[str]] | None) -> str:
    if not skills:
        return ""
    lines = []
    for category, items in skills.items():
        lines.append(f"{category}: {', '.join(items)}")
    return "\n".join(lines)


@app.route("/", methods=["GET"])
def index():
    data = load_data()
    skills_text = skills_to_text(data.get("skills"))
    return render_template("editor.html", data=data, skills_text=skills_text)


@app.route("/save", methods=["POST"])
def save():
    try:
        data = build_data_from_form()
        save_data(data)
        write_html_and_pdf(data)
        flash("CV mis à jour avec succès.", "success")
    except subprocess.CalledProcessError as e:
        flash(f"Erreur lors de la génération PDF : {e}", "error")
    except Exception as e:
        flash(f"Erreur inattendue : {e}", "error")

    return redirect(url_for("index"))


@app.route("/preview", methods=["GET"])
def preview():
    html_file = OUTPUT_DIR / "cv_output.html"
    if not html_file.exists():
        data = load_data()
        write_html_and_pdf(data)

    return redirect("/output/cv_output.html")


@app.route("/pdf", methods=["GET"])
def pdf():
    pdf_file = OUTPUT_DIR / "cv_output.pdf"
    if not pdf_file.exists():
        data = load_data()
        write_html_and_pdf(data)

    return redirect("/output/cv_output.pdf")


@app.route("/output/<path:filename>")
def output_file(filename: str):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    app.run(debug=True)