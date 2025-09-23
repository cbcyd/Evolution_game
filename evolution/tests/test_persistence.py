import os
from evolution.core.cell import Cell
from evolution.core.world import World
from evolution.services.persistence import save_world, load_world
from evolution.behaviors.strategies import random_walk_strategy

def test_save_and_load_world(tmp_path):
    """
    Tests that a world can be saved to and loaded from a file.
    Uses the pytest tmp_path fixture for clean, temporary file management.
    """
    # Setup
    test_filepath = tmp_path / "test_world.pkl"

    world = World(width=20, height=10)
    cell1 = Cell(energy=10.0, x=1, y=1, strategy=random_walk_strategy, genome=None)
    cell2 = Cell(energy=20.0, x=2, y=2, strategy=random_walk_strategy, genome=None)
    world.add_cell(cell1)
    world.add_cell(cell2)

    # Save the world
    save_world(world, test_filepath)

    # Check that the save file exists
    assert os.path.exists(test_filepath)

    # Load the world
    loaded_world = load_world(test_filepath)

    # Check that the loaded world is correct
    assert loaded_world is not None
    assert loaded_world.width == world.width
    assert loaded_world.height == world.height

    loaded_cells = list(loaded_world.cells)
    assert len(loaded_cells) == 2

    original_cells = list(world.cells)

    # Sort by a unique attribute to ensure consistent order for comparison
    loaded_cells.sort(key=lambda c: (c.x, c.y))
    original_cells.sort(key=lambda c: (c.x, c.y))

    assert loaded_cells == original_cells

    # No cleanup needed, pytest handles tmp_path
