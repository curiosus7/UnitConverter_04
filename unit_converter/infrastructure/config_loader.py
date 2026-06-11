"""Load unit ratios from JSON/YAML configuration files."""

import json
from pathlib import Path


class ConfigError(Exception):
    pass


def load_units_json(path: Path) -> dict[str, float]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(str(exc)) from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ConfigError(str(exc)) from exc

    if not isinstance(data, dict):
        raise ConfigError("Unit config must be a JSON object")

    units: dict[str, float] = {}
    for name, ratio in data.items():
        if not isinstance(name, str) or not isinstance(ratio, (int, float)):
            raise ConfigError("Unit config must map unit names to numbers")
        units[name] = float(ratio)

    return units
