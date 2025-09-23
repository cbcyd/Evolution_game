import pytest
from evolution.core.cell import Cell
from evolution.core.world import World

def test_cell_creation():
    cell = Cell(energy=10.0, x=5, y=5)
    assert cell.energy == 10.0
    assert cell.x == 5
    assert cell.y == 5

def test_cell_is_immutable():
    cell = Cell(energy=10.0, x=5, y=5)
    with pytest.raises(AttributeError):
        cell.energy = 20.0

def test_world_creation():
    world = World(width=100, height=50)
    assert world.width == 100
    assert world.height == 50
    assert len(list(world.cells)) == 0

def test_add_and_get_cell():
    world = World(width=10, height=10)
    cell = Cell(energy=10.0, x=5, y=5)
    world.add_cell(cell)
    retrieved_cell = world.get_cell(x=5, y=5)
    assert retrieved_cell is cell
    assert len(list(world.cells)) == 1

def test_add_cell_out_of_bounds():
    world = World(width=10, height=10)
    cell = Cell(energy=10.0, x=15, y=15)
    with pytest.raises(ValueError):
        world.add_cell(cell)

def test_remove_cell():
    world = World(width=10, height=10)
    cell = Cell(energy=10.0, x=5, y=5)
    world.add_cell(cell)
    assert world.get_cell(x=5, y=5) is not None
    world.remove_cell(cell)
    assert world.get_cell(x=5, y=5) is None
    assert len(list(world.cells)) == 0

def test_cells_property():
    world = World(width=10, height=10)
    cell1 = Cell(energy=10.0, x=1, y=1)
    cell2 = Cell(energy=10.0, x=2, y=2)
    world.add_cell(cell1)
    world.add_cell(cell2)

    cells_list = list(world.cells)
    assert len(cells_list) == 2
    assert cell1 in cells_list
    assert cell2 in cells_list
