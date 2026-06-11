"""Format conversion results for CLI output (SRP: presentation only)."""

import csv
import io
import json
import sys

VALID_FORMATS = frozenset({"table", "json", "csv"})


def format_conversion_line(
    unit: str, value: float, target_unit: str, converted: float
) -> str:
    return f"{value} {unit} = {converted:.4f} {target_unit}"


def format_conversion_lines(
    unit: str, value: float, results: dict[str, float],
) -> list[str]:
    return [
        format_conversion_line(unit, value, target_unit, converted)
        for target_unit, converted in results.items()
    ]


def format_conversion_output(
    unit: str, value: float, results: dict[str, float],
) -> str:
    return "\n".join(format_conversion_lines(unit, value, results)) + "\n"


def format_json_output(unit: str, value: float, results: dict[str, float]) -> str:
    payload = {
        "input": {"unit": unit, "value": value},
        "results": results,
    }
    return json.dumps(payload, indent=2) + "\n"


def format_csv_output(unit: str, value: float, results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["unit", "value"])
    for target_unit, converted in results.items():
        writer.writerow([target_unit, f"{converted:.4f}"])
    return buffer.getvalue()


def format_by_type(
    output_format: str,
    unit: str,
    value: float,
    results: dict[str, float],
) -> str:
    if output_format == "json":
        return format_json_output(unit, value, results)
    if output_format == "csv":
        return format_csv_output(unit, value, results)
    return format_conversion_output(unit, value, results)


def write_conversion(
    unit: str,
    value: float,
    results: dict[str, float],
    stream=None,
    output_format: str = "table",
) -> None:
    if stream is None:
        stream = sys.stdout
    stream.write(format_by_type(output_format, unit, value, results))


def write_message(message: str, stream=None) -> None:
    if stream is None:
        stream = sys.stdout
    stream.write(f"{message}\n")
