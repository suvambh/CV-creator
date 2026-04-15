from __future__ import annotations

import subprocess

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.dependencies import get_cv_service
from app.forms.form_parser import build_data_from_form, skills_to_text


editor_bp = Blueprint("editor", __name__)


@editor_bp.get("/")
def index():
    cv_service = get_cv_service()
    data = cv_service.load_cv()
    skills_text = skills_to_text(data.get("skills"))
    return render_template("editor.html", data=data, skills_text=skills_text)


@editor_bp.post("/save")
def save():
    cv_service = get_cv_service()

    try:
        data = build_data_from_form(request.form)
        cv_service.save_and_generate(data)
        flash("CV mis à jour avec succès.", "success")
    except subprocess.CalledProcessError as exc:
        flash(f"Erreur lors de la génération PDF : {exc}", "error")
    except Exception as exc:
        flash(f"Erreur inattendue : {exc}", "error")

    return redirect(url_for("editor.index"))