from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from exceptions import ValidationError


class JsonRepository:
    """Persistence component responsible for JSON storage and ID generation."""

    REQUIRED_KEYS = ("patients", "health_workers", "consultations")

    def __init__(self, data_file: str | Path):
        self._data_file = Path(data_file)
        self._data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self._data_file.exists():
            self.save({key: [] for key in self.REQUIRED_KEYS})

    def load(self) -> Dict[str, Any]:
        try:
            with self._data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"Data file '{self._data_file}' contains invalid JSON.") from exc

        if not isinstance(data, dict):
            raise ValidationError("Data file root must be a JSON object.")
        for key in self.REQUIRED_KEYS:
            if key not in data or not isinstance(data[key], list):
                raise ValidationError(f"Data file must contain a list named '{key}'.")
        return data

    def save(self, data: Dict[str, Any]) -> None:
        temp_file = self._data_file.with_suffix(self._data_file.suffix + ".tmp")
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        temp_file.replace(self._data_file)

    @staticmethod
    def next_id(existing_ids, prefix: str, width: int = 4) -> str:
        highest = 0
        for value in existing_ids:
            text = str(value).strip().upper()
            if text.startswith(prefix) and text[len(prefix):].isdigit():
                highest = max(highest, int(text[len(prefix):]))
        return f"{prefix}{highest + 1:0{width}d}"
