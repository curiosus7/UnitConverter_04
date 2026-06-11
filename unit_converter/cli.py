import sys

from unit_converter.app.input_parser import ParseError, parse
from unit_converter.domain.converter import convert_all
from unit_converter.domain.unit_registry import UnknownUnitError


def main(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    input_str = args[0] if args else ""

    try:
        unit, value = parse(input_str)
        results = convert_all(unit, value)
        for target_unit, converted in results.items():
            print(f"{value} {unit} = {converted:.4f} {target_unit}")
    except (ParseError, UnknownUnitError) as exc:
        print(str(exc))
