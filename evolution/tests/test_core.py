import pytest
from evolution.core.cell import Cell
from evolution.core.world import World
from evolution.behaviors.strategies import random_walk_strategy

def test_cell_creation():
    cell = Cell(energy=10.0, x=5, y=5, strategy=random_walk_strategy, genome=None)
    assert cell.energy == 10.0
    assert cell.x == 5
    assert cell.y == 5
    assert cell.is_alive is True

def test_negative_energy_raises_value_error():
    with pytest.raises(ValueError):
        Cell(energy=-10.0, x=5, y=5, strategy=random_walk_strategy, genome=None)

def test_world_creation():
    world = World(width=100, height=50)
    assert world.width == 100
    assert world.height == 50
    assert len(list(world.cells)) == 0

def test_add_and_get_cell():
    world = World(width=10, height=10)
    cell = Cell(energy=10.0, x=5, y=5, strategy=random_walk_strategy, genome=None)
    world.add_cell(cell)
    retrieved_cell = world.get_cell(x=5, y=5)
    assert retrieved_cell is cell
    assert len(list(world.cells)) == 1

def test_add_cell_out_of_bounds():
    world = World(width=10, height=10)
    cell = Cell(energy=10.0, x=15, y=15, strategy=random_walk_strategy, genome=None)
    with pytest.raises(ValueError):
        world.add_cell(cell)

def test_remove_cell():
    world = World(width=10, height=10)
    cell = Cell(energy=10.0, x=5, y=5, strategy=random_walk_strategy, genome=None)
    world.add_cell(cell)
    assert world.get_cell(x=5, y=5) is not None
    world.remove_cell(cell)
    assert world.get_cell(x=5, y=5) is None
    assert len(list(world.cells)) == 0

def test_cells_property():
    world = World(width=10, height=10)
    cell1 = Cell(energy=10.0, x=1, y=1, strategy=random_walk_strategy, genome=None)
    cell2 = Cell(energy=10.0, x=2, y=2, strategy=random_walk_strategy, genome=None)
    world.add_cell(cell1)
    world.add_cell(cell2)

    cells_list = list(world.cells)
    assert len(cells_list) == 2
    assert cell1 in cells_list
    assert cell2 in cells_list
