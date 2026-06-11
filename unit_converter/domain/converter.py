from unit_converter.domain.unit_registry import UnitRegistry


def to_meter(unit: str, value: float, registry: UnitRegistry | None = None) -> float:
    if registry is None:
        registry = UnitRegistry.default()
    ratio = registry.get_ratio(unit)
    return value / ratio


def convert_all(
    unit: str,
    value: float,
    registry: UnitRegistry | None = None,
) -> dict[str, float]:
    if registry is None:
        registry = UnitRegistry.default()
    meter_value = to_meter(unit, value, registry)
    return {
        name: round(meter_value * ratio, 4)
        for name, ratio in registry.all_units().items()
    }
