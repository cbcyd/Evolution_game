"""
This module contains the action classes for the simulation.
Actions are yielded by cell brains and executed by the simulation loop.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class MoveAction:
    """An action for a cell to move to a new position."""
    dx: int
    dy: int

@dataclass(frozen=True)
class EatAction:
    """An action for a cell to eat."""
    pass

@dataclass(frozen=True)
class DivideAction:
    """An action for a cell to divide."""
    pass
