import random
import neat
from evolution.core.actions import MoveAction, DivideAction, EatAction
from evolution.core.constants import DIVISION_THRESHOLD

def random_walk_strategy(cell, world, neat_config=None):
    """A simple strategy where the cell moves randomly and divides."""
    while True:
        if cell.energy >= DIVISION_THRESHOLD:
            yield DivideAction()

        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        yield MoveAction(dx, dy)

def neat_strategy(cell, world, neat_config):
    """A strategy that uses a NEAT-evolved neural network to decide actions."""
    net = neat.nn.FeedForwardNetwork.create(cell.genome, neat_config)

    while True:
        inputs = [
            cell.energy,
            cell.x / world.width,
            cell.y / world.height,
            1.0,  # Bias node
        ]

        outputs = net.activate(inputs)

        action_index = outputs.index(max(outputs))

        if action_index == 0:
            # Move action: map a single output to dx, dy. This is a simplification.
            # A better approach would be to have separate outputs for dx and dy.
            dx = int(round(outputs[0] * 2 - 1))
            dy = int(round(outputs[1] * 2 - 1)) if len(outputs) > 3 else int(round(outputs[0] * 2 - 1)) # simplified
            yield MoveAction(dx, dy)
        elif action_index == 1:
            yield EatAction()
        elif action_index == 2:
            yield DivideAction()
        else:
            # Idle
            yield MoveAction(0, 0)
