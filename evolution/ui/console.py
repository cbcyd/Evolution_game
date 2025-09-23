import os
from evolution.core.world import World

def display_world(world: World):
    """Clears the console and prints the current state of the world."""
    os.system('cls' if os.name == 'nt' else 'clear')

    grid = [['.' for _ in range(world.width)] for _ in range(world.height)]

    for cell in world.cells:
        if 0 <= cell.x < world.width and 0 <= cell.y < world.height:
            grid[cell.y][cell.x] = 'O'

    for row in grid:
        print(' '.join(row))
