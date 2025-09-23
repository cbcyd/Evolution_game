from evolution.core.descriptors import NonNegative
from typing import Generator, Callable

class Cell:
    """
    Represents a single cell in the simulation.

    Attributes:
        energy (float): The energy level of the cell.
        x (int): The x-coordinate of the cell in the world.
        y (int): The y-coordinate of the cell in the world.
        strategy (Callable[..., Generator]): The behavior strategy of the cell.
        genome: The genome of the cell, used by NEAT.
        brain (Generator): The generator that produces actions for the cell.
        is_alive (bool): A flag indicating if the cell is alive.
    """
    __slots__ = ['_energy', 'x', 'y', 'is_alive', 'strategy', 'brain', 'genome']

    energy = NonNegative()

    def __init__(self, energy: float, x: int, y: int, strategy: Callable[..., Generator], genome):
        self.energy = energy
        self.x = x
        self.y = y
        self.strategy = strategy
        self.genome = genome
        self.brain = None  # Will be initialized by the simulation
        self.is_alive = True

    def __repr__(self):
        return f"Cell(energy={self.energy}, x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented
        # Not comparing brain, as it's a generator
        return (self.energy, self.x, self.y, self.is_alive, self.strategy, self.genome) == \
               (other.energy, other.x, other.y, other.is_alive, other.strategy, other.genome)

    def __hash__(self):
        # Not hashing brain
        return hash((self.energy, self.x, self.y, self.is_alive, self.strategy, self.genome))
