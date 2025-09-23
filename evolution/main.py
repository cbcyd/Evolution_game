import time
from evolution.core.cell import Cell
from evolution.core.world import World
from evolution.engine.loop import Simulation
from evolution.ui.console import display_world
from evolution.core.constants import INITIAL_CELL_ENERGY

def main():
    """Main function to run the simulation."""
    world = World(width=40, height=20)

    # Add some initial cells
    world.add_cell(Cell(energy=INITIAL_CELL_ENERGY, x=10, y=10))
    world.add_cell(Cell(energy=INITIAL_CELL_ENERGY, x=20, y=10))
    world.add_cell(Cell(energy=INITIAL_CELL_ENERGY, x=30, y=10))

    simulation = Simulation(world)

    for i in range(100):
        simulation.step()
        display_world(world)
        print(f"Tick: {i+1}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
