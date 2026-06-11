"""Parse dynamic unit registration expressions (EXT-02)."""

import re

REGISTER_PATTERN = re.compile(
    r"^\s*1\s+(\w+)\s*=\s*([0-9.]+)\s+meter\s*$",
    re.IGNORECASE,
)


class RegisterParseError(Exception):
    pass


def parse_register_expression(expression: str) -> tuple[str, float]:
    match = REGISTER_PATTERN.match(expression.strip())
    if not match:
        raise RegisterParseError(
            "Invalid register format. Use: 1 cubit = 0.4572 meter"
        )
    return match.group(1).lower(), float(match.group(2))
