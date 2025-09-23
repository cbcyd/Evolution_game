from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Cell:
    """Represents the state of a single cell."""
    energy: float
    x: int
    y: int
