import os
import neat
from evolution.core.cell import Cell
from evolution.core.world import World
from evolution.engine.loop import Simulation
from evolution.behaviors.strategies import random_walk_strategy
from evolution.services.event_bus import EventBus

def test_simulation_step_division():
    # Setup
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'neat.cfg')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    world = World(width=10, height=10)
    event_bus = EventBus()

    # Create a cell with enough energy to divide
    cell = Cell(energy=10.1, x=5, y=5, strategy=random_walk_strategy, genome=None)
    world.add_cell(cell)

    simulation = Simulation(world, event_bus, config)

    # Run one step
    simulation.step()

    # The parent cell should be gone, and there should be two new cells.
    assert len(list(world.cells)) == 2

    # Check that the total energy is conserved
    total_energy = sum(c.energy for c in world.cells)
    # The parent cell had 10.1 energy, consumed 0.1, so 10.0 remaining.
    # The two daughters should have 5.0 each. Total 10.0.
    assert total_energy == 10.0
