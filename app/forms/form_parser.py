from __future__ import annotations

from typing import Any, Mapping


def split_lines(text: str) -> list[str]:
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_skills(raw_text: str) -> dict[str, list[str]]:
    """
    Expects lines like:
    Languages: Python, SQL, Bash
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


def _getlist(form: Mapping[str, Any], key: str) -> list[str]:
    getter = getattr(form, "getlist", None)
    if callable(getter):
        return getter(key)
    value = form.get(key, [])
    if isinstance(value, list):
        return value
    if value == "":
        return []
    return [value]


def collect_entries(form: Mapping[str, Any], prefix: str) -> list[dict[str, Any]]:
    roles = _getlist(form, f"{prefix}_role[]")
    companies = _getlist(form, f"{prefix}_company[]")
    durations = _getlist(form, f"{prefix}_duration[]")
    locations = _getlist(form, f"{prefix}_location[]")
    techs = _getlist(form, f"{prefix}_tech[]")
    details_list = _getlist(form, f"{prefix}_details[]")

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


def collect_projects(form: Mapping[str, Any]) -> list[dict[str, Any]]:
    names = _getlist(form, "project_name[]")
    techs = _getlist(form, "project_tech[]")
    details_list = _getlist(form, "project_details[]")

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


def collect_education(form: Mapping[str, Any]) -> list[dict[str, Any]]:
    degrees = _getlist(form, "education_degree[]")
    institutions = _getlist(form, "education_institution[]")
    years = _getlist(form, "education_year[]")

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


def collect_certifications(form: Mapping[str, Any]) -> list[dict[str, Any]]:
    names = _getlist(form, "cert_name[]")
    issuers = _getlist(form, "cert_issuer[]")
    years = _getlist(form, "cert_year[]")

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


def build_data_from_form(form: Mapping[str, Any]) -> dict[str, Any]:
    data: dict[str, Any] = {}

    for field in [
        "name",
        "title",
        "photo",
        "email",
        "phone",
        "location",
        "linkedin",
        "github",
        "summary",
    ]:
        value = str(form.get(field, "")).strip()
        if value:
            data[field] = value

    skills_raw = str(form.get("skills_text", "")).strip()
    skills = parse_skills(skills_raw)
    if skills:
        data["skills"] = skills

    experience = collect_entries(form, "experience")
    if experience:
        data["experience"] = experience

    projects = collect_projects(form)
    if projects:
        data["projects"] = projects

    education = collect_education(form)
    if education:
        data["education"] = education

    certifications = collect_certifications(form)
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