from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CVRepository:
    """Read and write CV data from a JSON file."""

    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file

    def load(self) -> dict[str, Any]:
        """Load CV data from JSON. Return empty dict if file is missing or blank."""
        if not self.data_file.exists():
            return {}

        raw = self.data_file.read_text(encoding="utf-8").strip()
        if not raw:
            return {}

        return json.loads(raw)

    def save(self, data: dict[str, Any]) -> None:
        """Persist CV data to JSON."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )