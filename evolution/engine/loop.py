import random
from evolution.core.world import World
from evolution.core.cell import Cell
from evolution.core.actions import MoveAction, EatAction, DivideAction
from evolution.services.event_bus import EventBus
from evolution.core.events import CellDiedEvent, CellDividedEvent
from evolution.core.constants import DIVISION_THRESHOLD, ENERGY_PER_TICK

class Simulation:
    def __init__(self, world: World, event_bus: EventBus, neat_config):
        self.world = world
        self.event_bus = event_bus
        self.neat_config = neat_config
        for cell in self.world.cells:
            cell.brain = cell.strategy(cell, self.world, self.neat_config)

    def step(self):
        for cell in list(self.world.cells):
            if not cell.is_alive:
                continue

            new_energy = cell.energy - ENERGY_PER_TICK
            if new_energy <= 0:
                cell.is_alive = False
                self.world.remove_cell(cell)
                self.event_bus.publish(CellDiedEvent(cell=cell))
                continue
            else:
                cell.energy = new_energy

            action = next(cell.brain)

            if isinstance(action, MoveAction):
                self._execute_move_action(cell, action)
            elif isinstance(action, DivideAction):
                self._execute_divide_action(cell)
            else:
                cell.energy = new_energy

    def _execute_move_action(self, cell, action: MoveAction):
        new_x = cell.x + action.dx
        new_y = cell.y + action.dy

        if 0 <= new_x < self.world.width and 0 <= new_y < self.world.height:
            if self.world.get_cell(new_x, new_y) is None:
                self.world.remove_cell(cell)
                cell.x = new_x
                cell.y = new_y
                self.world.add_cell(cell)

    def _execute_divide_action(self, parent_cell):
        if parent_cell.energy < DIVISION_THRESHOLD:
            return

        # Simple placement logic, does not handle collisions yet
        daughter_pos1 = self._find_empty_neighbor(parent_cell.x, parent_cell.y)
        if not daughter_pos1:
            return

        daughter_pos2 = self._find_empty_neighbor(parent_cell.x, parent_cell.y, exclude=[daughter_pos1])
        if not daughter_pos2:
            return

        daughter_energy = parent_cell.energy / 2

        child1 = Cell(energy=daughter_energy, x=daughter_pos1[0], y=daughter_pos1[1], strategy=parent_cell.strategy, genome=parent_cell.genome)
        child2 = Cell(energy=daughter_energy, x=daughter_pos2[0], y=daughter_pos2[1], strategy=parent_cell.strategy, genome=parent_cell.genome)
        child1.brain = child1.strategy(child1, self.world, self.neat_config)
        child2.brain = child2.strategy(child2, self.world, self.neat_config)

        self.world.remove_cell(parent_cell)
        self.world.add_cell(child1)
        self.world.add_cell(child2)

        self.event_bus.publish(CellDividedEvent(parent=parent_cell, child1=child1, child2=child2))

    def _find_empty_neighbor(self, x, y, exclude=None):
        if exclude is None:
            exclude = []
        neighbors = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y),                 (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        ]
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if (nx,ny) in exclude:
                continue
            if 0 <= nx < self.world.width and 0 <= ny < self.world.height:
                if self.world.get_cell(nx, ny) is None:
                    return (nx, ny)
        return None

    def shutdown(self):
        pass
