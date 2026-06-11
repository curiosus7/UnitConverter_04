"""Shared conversion orchestration for CLI and GUI."""

from pathlib import Path

from unit_converter.app.input_parser import ParseError, parse
from unit_converter.app.output_formatter import format_by_type
from unit_converter.app.register_parser import RegisterParseError, parse_register_expression
from unit_converter.domain.converter import convert_all
from unit_converter.domain.unit_registry import UnitRegistry, UnknownUnitError
from unit_converter.infrastructure.config_loader import ConfigError, load_units_json


def build_registry(
    units_file: Path | None = None,
    register_expressions: list[str] | None = None,
) -> UnitRegistry:
    if units_file is not None:
        registry = UnitRegistry.from_units(load_units_json(units_file))
    else:
        registry = UnitRegistry.default()

    if register_expressions:
        for expression in register_expressions:
            name, meters_per_unit = parse_register_expression(expression)
            registry.register_meters_per_unit(name, meters_per_unit)

    return registry


def convert_input(
    unit: str,
    value: float,
    output_format: str = "table",
    registry: UnitRegistry | None = None,
) -> str:
    results = convert_all(unit, value, registry=registry)
    return format_by_type(output_format, unit, value, results)


def convert_cli_string(
    input_str: str,
    output_format: str = "table",
    registry: UnitRegistry | None = None,
) -> str:
    unit, value = parse(input_str)
    return convert_input(unit, value, output_format, registry=registry)


__all__ = [
    "ParseError",
    "RegisterParseError",
    "ConfigError",
    "UnknownUnitError",
    "build_registry",
    "convert_cli_string",
    "convert_input",
    "parse",
]
