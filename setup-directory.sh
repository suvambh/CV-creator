#!/usr/bin/env bash

set -e

BASE_DIR="."

echo "📁 Creating project structure in: $BASE_DIR"

# ---------- helpers ----------

create_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo "✅ Created directory: $1"
    else
        echo "⏭️  Skipped existing directory: $1"
    fi
}

create_file() {
    if [ ! -f "$1" ]; then
        mkdir -p "$(dirname "$1")"
        touch "$1"
        echo "✅ Created file: $1"
    else
        echo "⏭️  Skipped existing file: $1"
    fi
}

create_file_with_content() {
    if [ ! -f "$1" ]; then
        mkdir -p "$(dirname "$1")"
        echo "$2" > "$1"
        echo "✅ Created file with content: $1"
    else
        echo "⏭️  Skipped existing file: $1"
    fi
}

# ---------- directories ----------

create_dir "$BASE_DIR/app/routes"
create_dir "$BASE_DIR/app/services"
create_dir "$BASE_DIR/app/repositories"
create_dir "$BASE_DIR/app/forms"
create_dir "$BASE_DIR/app/models"
create_dir "$BASE_DIR/app/templates"
create_dir "$BASE_DIR/app/static"

create_dir "$BASE_DIR/data"
create_dir "$BASE_DIR/output"
create_dir "$BASE_DIR/scripts"
create_dir "$BASE_DIR/tests"

# ---------- app core files ----------

create_file "$BASE_DIR/app/__init__.py"
create_file "$BASE_DIR/app/config.py"

# routes
create_file "$BASE_DIR/app/routes/__init__.py"
create_file "$BASE_DIR/app/routes/editor.py"
create_file "$BASE_DIR/app/routes/preview.py"

# services
create_file "$BASE_DIR/app/services/__init__.py"
create_file "$BASE_DIR/app/services/cv_service.py"
create_file "$BASE_DIR/app/services/render_service.py"
create_file "$BASE_DIR/app/services/pdf_service.py"

# repositories
create_file "$BASE_DIR/app/repositories/__init__.py"
create_file "$BASE_DIR/app/repositories/cv_repository.py"

# forms
create_file "$BASE_DIR/app/forms/__init__.py"
create_file "$BASE_DIR/app/forms/form_parser.py"

# models
create_file "$BASE_DIR/app/models/__init__.py"
create_file "$BASE_DIR/app/models/cv.py"
create_file "$BASE_DIR/app/models/experience.py"
create_file "$BASE_DIR/app/models/project.py"
create_file "$BASE_DIR/app/models/education.py"
create_file "$BASE_DIR/app/models/certification.py"

# ---------- root files ----------

create_file_with_content "$BASE_DIR/data/data.json" "{}"

create_file "$BASE_DIR/scripts/generate_cv.py"

create_file "$BASE_DIR/tests/__init__.py"
create_file "$BASE_DIR/tests/test_form_parser.py"
create_file "$BASE_DIR/tests/test_render_service.py"
create_file "$BASE_DIR/tests/test_repository.py"

create_file "$BASE_DIR/run.py"
create_file "$BASE_DIR/requirements.txt"

echo ""
echo "🎉 Structure setup complete!"
