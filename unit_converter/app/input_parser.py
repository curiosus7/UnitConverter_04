E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"
E_NUM = "Invalid number: {value_str}"
E_NEG = "Negative value not allowed"


class ParseError(Exception):
    pass


def parse(s: str) -> tuple[str, float]:
    if ":" not in s:
        raise ParseError(E_FMT)

    unit, value_str = s.split(":", 1)

    if not unit or not value_str:
        raise ParseError(E_FMT)

    try:
        value = float(value_str)
    except ValueError:
        raise ParseError(E_NUM.format(value_str=value_str))

    if value < 0:
        raise ParseError(E_NEG)

    return unit, value
