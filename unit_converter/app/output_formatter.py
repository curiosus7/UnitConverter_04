"""Format conversion results for CLI output (SRP: presentation only)."""

import sys


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


def write_conversion(
    unit: str,
    value: float,
    results: dict[str, float],
    stream=None,
) -> None:
    if stream is None:
        stream = sys.stdout
    stream.write(format_conversion_output(unit, value, results))


def write_message(message: str, stream=None) -> None:
    if stream is None:
        stream = sys.stdout
    stream.write(f"{message}\n")
