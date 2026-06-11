"""Format conversion results for CLI output (SRP: presentation only)."""

import csv
import io
import json
import sys

VALID_FORMATS = frozenset({"table", "json", "csv"})

TABLE_COL_WIDTHS = (8, 9, 9)


def format_display_number(value: float) -> str:
    """Natural display for input column (2.5, 10)."""
    rounded = round(value, 4)
    fixed = f"{rounded:.4f}"
    if fixed.endswith("0000"):
        return fixed[:-5]
    return fixed.rstrip("0").rstrip(".")


def format_result_number(converted: float, input_value: float) -> str:
    """Result column: match appendix (2.5 / 8.2021 / 2.7340)."""
    rounded = round(converted, 4)
    if rounded == round(input_value, 4):
        return format_display_number(input_value)
    return f"{rounded:.4f}"


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


def _table_cell(text: str, width: int, *, align: str) -> str:
    inner = width - 1
    if align == "left":
        return f" {text:<{inner}}"
    return f" {text:>{inner}}"


def _table_row(unit: str, input_text: str, result_text: str) -> str:
    alignments = ("left", "right", "right")
    texts = (unit, input_text, result_text)
    cells = [
        _table_cell(text, width, align=align)
        for text, width, align in zip(texts, TABLE_COL_WIDTHS, alignments)
    ]
    return f"│{cells[0]}│{cells[1]}│{cells[2]}│"


def format_table_output(
    unit: str, value: float, results: dict[str, float],
) -> str:
    """Lecture appendix: box-drawing table (--format table)."""
    segments = ["─" * width for width in TABLE_COL_WIDTHS]
    horiz = "┬".join(segments)
    top = f"┌{horiz}┐"
    header = _table_row("unit", "input", "result")
    divider = f"├{'┼'.join(segments)}┤"
    bottom = f"└{'┴'.join(segments)}┘"

    input_text = format_display_number(value)
    data_rows = [
        _table_row(
            target_unit,
            input_text,
            format_result_number(converted, value),
        )
        for target_unit, converted in results.items()
    ]

    return "\n".join([top, header, divider, *data_rows, bottom]) + "\n"


def format_json_output(unit: str, value: float, results: dict[str, float]) -> str:
    payload = {
        "input": {"unit": unit, "value": value},
        "results": results,
    }
    return json.dumps(payload, indent=2) + "\n"


def format_csv_output(unit: str, value: float, results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["unit", "input", "result"])
    input_text = format_display_number(value)
    for target_unit, converted in results.items():
        writer.writerow(
            [target_unit, input_text, format_result_number(converted, value)]
        )
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
    return format_table_output(unit, value, results)


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
