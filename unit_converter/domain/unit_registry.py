class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, float] = {
            "meter": 1.0,
            "feet": 3.28084,
            "yard": 1.09361,
        }

    def get_ratio(self, name: str) -> float:
        return self._units[name]

    def all_units(self) -> dict[str, float]:
        return dict(self._units)

    @classmethod
    def default(cls) -> "UnitRegistry":
        return cls()
