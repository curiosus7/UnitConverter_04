import sys

from unit_converter.app.input_parser import ParseError, parse


def main(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    input_str = args[0] if args else ""

    try:
        parse(input_str)
    except ParseError as exc:
        print(str(exc))
