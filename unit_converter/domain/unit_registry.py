class UnknownUnitError(Exception):
    pass


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, float] = {}

    def register(self, name: str, ratio_per_meter: float) -> None:
        self._units[name] = ratio_per_meter

    def register_meters_per_unit(self, name: str, meters_per_unit: float) -> None:
        if meters_per_unit <= 0:
            raise ValueError("meters_per_unit must be positive")
        self.register(name, 1.0 / meters_per_unit)

    @classmethod
    def from_units(cls, units: dict[str, float]) -> "UnitRegistry":
        registry = cls()
        for name, ratio in units.items():
            registry.register(name, ratio)
        return registry

    def get_ratio(self, name: str) -> float:
        if name not in self._units:
            raise UnknownUnitError(f"Unknown unit: {name}")
        return self._units[name]

    def all_units(self) -> dict[str, float]:
        return dict(self._units)

    @classmethod
    def default(cls) -> "UnitRegistry":
        registry = cls()
        registry.register("meter", 1.0)
        registry.register("feet", 3.28084)
        registry.register("yard", 1.09361)
        return registry
