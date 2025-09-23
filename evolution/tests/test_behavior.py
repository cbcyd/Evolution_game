import neat
import os
from evolution.core.cell import Cell
from evolution.core.world import World
from evolution.behaviors.strategies import random_walk_strategy, neat_strategy
from evolution.core.actions import MoveAction, DivideAction
from evolution.core.constants import DIVISION_THRESHOLD

def test_random_walk_strategy_divides_when_energy_is_high():
    cell = Cell(energy=DIVISION_THRESHOLD, x=5, y=5, strategy=random_walk_strategy, genome=None)
    # The world is not used by this simple strategy, so it can be None
    cell.brain = cell.strategy(cell, None)

    action = next(cell.brain)
    assert isinstance(action, DivideAction)

def test_random_walk_strategy_moves_when_energy_is_low():
    cell = Cell(energy=DIVISION_THRESHOLD - 1, x=5, y=5, strategy=random_walk_strategy, genome=None)
    # The world is not used by this simple strategy, so it can be None
    cell.brain = cell.strategy(cell, None)

    action = next(cell.brain)
    assert isinstance(action, MoveAction)
    assert -1 <= action.dx <= 1
    assert -1 <= action.dy <= 1
