import sys
from pathlib import Path

from unit_converter.app.conversion_service import (
    ConfigError,
    ParseError,
    RegisterParseError,
    UnknownUnitError,
    build_registry,
)
from unit_converter.app.input_parser import parse
from unit_converter.app.output_formatter import VALID_FORMATS, write_conversion, write_message
from unit_converter.domain.converter import convert_all


def _parse_cli_args(args: list[str]) -> tuple[list[str], str, str | None, list[str]]:
    output_format = "table"
    units_file: str | None = None
    register_expressions: list[str] = []
    positional: list[str] = []

    index = 0
    while index < len(args):
        token = args[index]
        if token == "--format" and index + 1 < len(args):
            output_format = args[index + 1]
            index += 2
            continue
        if token == "--units-file" and index + 1 < len(args):
            units_file = args[index + 1]
            index += 2
            continue
        if token == "--register" and index + 1 < len(args):
            register_expressions.append(args[index + 1])
            index += 2
            continue
        positional.append(token)
        index += 1

    return positional, output_format, units_file, register_expressions


def main(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    positional, output_format, units_file, register_expressions = _parse_cli_args(args)
    input_str = positional[0] if positional else ""

    if output_format not in VALID_FORMATS:
        write_message(
            f"Invalid format option. Use: {', '.join(sorted(VALID_FORMATS))}"
        )
        return

    try:
        registry = build_registry(
            Path(units_file) if units_file else None,
            register_expressions or None,
        )
        unit, value = parse(input_str)
        results = convert_all(unit, value, registry=registry)
        write_conversion(unit, value, results, output_format=output_format)
    except (ParseError, UnknownUnitError, RegisterParseError, ConfigError) as exc:
        write_message(str(exc))
