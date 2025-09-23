"""
This module contains the event classes for the simulation.
"""
from dataclasses import dataclass
from evolution.core.cell import Cell

@dataclass
class Event:
    """Base class for events."""
    pass

@dataclass
class CellDiedEvent(Event):
    """Event published when a cell dies."""
    cell: Cell

@dataclass
class CellDividedEvent(Event):
    """Event published when a cell divides."""
    parent: Cell
    child1: Cell
    child2: Cell
