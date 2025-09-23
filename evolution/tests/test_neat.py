import os
import neat
from evolution.core.cell import Cell
from evolution.core.world import World
from evolution.behaviors.strategies import neat_strategy
from evolution.core.actions import MoveAction, EatAction, DivideAction

def test_neat_strategy():
    # Load configuration.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '..', '..', 'neat.cfg')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create a dummy genome.
    genome = neat.DefaultGenome(0)
    genome.configure_new(config.genome_config)

    # Create a cell with the neat_strategy.
    cell = Cell(energy=10.0, x=5, y=5, strategy=neat_strategy, genome=genome)
    world = World(width=10, height=10)
    world.add_cell(cell)

    # Initialize the brain.
    cell.brain = cell.strategy(cell, world, config)

    # Get an action from the brain.
    action = next(cell.brain)

    assert isinstance(action, (MoveAction, EatAction, DivideAction))
