# CV Creator

## Overview

CV Creator is a Flask-based web application for generating CVs from structured data. It provides a browser-based editor to input and modify CV content, renders the data into HTML using Jinja2 templates, and exports the result as a PDF via WeasyPrint.

The system is designed with a layered architecture separating presentation, application logic, and infrastructure concerns.

---

## Architecture

The project follows a modular structure:

```
cv_creator/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── config.py            # Configuration and paths
│   ├── dependencies.py      # Service construction
│   ├── routes/              # Flask blueprints
│   ├── services/            # Application services
│   ├── repositories/        # Data access layer
│   ├── forms/               # Form parsing logic
│   ├── models/              # (Optional) domain models
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS and JS assets
├── data/                    # JSON data storage
├── output/                  # Generated HTML and PDF
├── run.py                   # Application entry point
└── requirements.txt
```

---

## Execution Flow

### 1. User Interaction

* User accesses `/`
* Form is rendered using `editor.html`
* Existing data is loaded from `data/data.json`

### 2. Form Submission

* POST `/save`
* Form data is parsed into structured format
* Data is persisted to JSON

### 3. Rendering Pipeline

* Data is passed to `RenderService`
* Jinja template (`cv.html`) produces HTML
* HTML is written to `output/cv_output.html`

### 4. PDF Generation

* `PDFService` invokes WeasyPrint
* HTML is converted to `output/cv_output.pdf`

### 5. Preview

* `/preview` → serves HTML
* `/pdf` → serves PDF

---

## Core Components

### 1. Repository Layer

**File:** `app/repositories/cv_repository.py`

Responsibilities:

* Load CV data from JSON
* Persist structured CV data

Interface:

```python
load() -> dict
save(data: dict) -> None
```

---

### 2. Service Layer

#### CVService

**File:** `app/services/cv_service.py`

Coordinates:

* Data persistence
* HTML rendering
* PDF generation

Key methods:

```python
load_cv()
save_cv(data)
generate_outputs(data)
save_and_generate(data)
ensure_preview_exists()
```

---

#### RenderService

**File:** `app/services/render_service.py`

Responsibilities:

* Initialize Jinja2 environment
* Render template with data
* Write HTML output

---

#### PDFService

**File:** `app/services/pdf_service.py`

Responsibilities:

* Execute WeasyPrint
* Convert HTML to PDF

Uses subprocess invocation of the WeasyPrint binary.

---

### 3. Form Parsing Layer

**File:** `app/forms/form_parser.py`

Responsibilities:

* Convert `request.form` into structured data
* Normalize repeated sections:

  * experience
  * projects
  * education
  * certifications
* Parse skills into categorized format

Design:

* Uses list-based extraction via `getlist`
* Filters empty entries
* Produces clean JSON-compatible structure

---

### 4. Routing Layer

#### Editor Routes

**File:** `app/routes/editor.py`

Endpoints:

* `GET /` → render editor
* `POST /save` → process form and regenerate outputs

---

#### Preview Routes

**File:** `app/routes/preview.py`

Endpoints:

* `GET /preview` → HTML output
* `GET /pdf` → PDF output
* `GET /output/<filename>` → static file serving

---

### 5. Dependency Construction

**File:** `app/dependencies.py`

Centralizes creation of:

* CVRepository
* RenderService
* PDFService
* CVService

Removes duplication across route modules.

---

## Data Model

The application operates on a structured JSON schema:

```json
{
  "name": "",
  "title": "",
  "email": "",
  "phone": "",
  "location": "",
  "linkedin": "",
  "github": "",
  "summary": "",
  "skills": {
    "Category": ["item1", "item2"]
  },
  "experience": [
    {
      "role": "",
      "company": "",
      "duration": "",
      "location": "",
      "tech": "",
      "details": []
    }
  ],
  "projects": [
    {
      "name": "",
      "tech": "",
      "details": []
    }
  ],
  "education": [
    {
      "degree": "",
      "institution": "",
      "year": ""
    }
  ],
  "certifications": [
    {
      "name": "",
      "issuer": "",
      "year": ""
    }
  ]
}
```

---

## Frontend Design

### Editor Template

* Located in `app/templates/editor.html`
* Uses Jinja2 for data binding
* Dynamic sections:

  * experience
  * projects
  * education
  * certifications

### Static Assets

* `editor.css` → layout and styling
* `editor.js` → dynamic form behavior

Key features:

* Template-based insertion (`<template>`)
* Generic add/remove logic
* Section-aware empty state handling

---

## Configuration

**File:** `app/config.py`

Defines:

* Base paths
* Template directory
* Output directory
* Data file location
* Default theme
* WeasyPrint binary path

Example:

```python
BASE_DIR = Path(...)
TEMPLATES_DIR = ...
OUTPUT_DIR = ...
DATA_FILE = ...
DEFAULT_THEME = "style.css"
WEASYPRINT_BIN = "/usr/bin/weasyprint"
```

---

## Dependencies

* Flask
* Jinja2
* WeasyPrint
* Python standard library (json, pathlib, subprocess)

---

## Running the Application

From project root:

```bash
python run.py
```

Then open:

```
http://127.0.0.1:5000/
```

---

## Design Considerations

### Separation of Concerns

* Routes are thin
* Business logic is in services
* Persistence is isolated
* Form parsing is centralized

### Idempotent Output Generation

* Outputs are regenerated on save
* Preview ensures existence without duplication

### Extensibility

* New sections can be added via:

  * form parser
  * template
  * JSON schema

### Trade-offs

* Uses dicts instead of typed models (simpler, less strict)
* Uses subprocess for PDF generation (system dependency)
* No database (file-based persistence)

---
