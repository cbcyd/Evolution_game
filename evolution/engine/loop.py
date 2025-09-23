import random
from typing import List, Tuple

from evolution.core.cell import Cell
from evolution.core.constants import DIVISION_THRESHOLD, ENERGY_PER_TICK
from evolution.core.world import World


class Simulation:
    def __init__(self, world: World):
        self.world = world

    def _find_empty_neighbor(self, x: int, y: int, start_from: Tuple[int, int] | None = None) -> Tuple[int, int] | None:
        neighbors = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y),                 (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        ]

        random.shuffle(neighbors)

        for nx, ny in neighbors:
            if 0 <= nx < self.world.width and 0 <= ny < self.world.height:
                if self.world.get_cell(nx, ny) is None:
                    if start_from and (nx, ny) == start_from:
                        continue
                    return nx, ny
        return None

    def step(self):
        cells_to_add: List[Cell] = []
        cells_to_remove: List[Cell] = []

        current_cells = list(self.world.cells)

        for cell in current_cells:
            new_energy = cell.energy - ENERGY_PER_TICK

            if new_energy <= 0:
                cells_to_remove.append(cell)
                continue

            if new_energy >= DIVISION_THRESHOLD:
                cells_to_remove.append(cell)

                daughter1_energy = new_energy / 2
                daughter2_energy = new_energy / 2

                daughter1_pos = self._find_empty_neighbor(cell.x, cell.y)
                if daughter1_pos:
                    cells_to_add.append(Cell(energy=daughter1_energy, x=daughter1_pos[0], y=daughter1_pos[1]))

                    daughter2_pos = self._find_empty_neighbor(cell.x, cell.y, start_from=daughter1_pos)
                    if daughter2_pos:
                        cells_to_add.append(Cell(energy=daughter2_energy, x=daughter2_pos[0], y=daughter2_pos[1]))
            else:
                cells_to_remove.append(cell)
                cells_to_add.append(Cell(energy=new_energy, x=cell.x, y=cell.y))

        for cell in cells_to_remove:
            if self.world.get_cell(cell.x, cell.y) == cell:
                self.world.remove_cell(cell)

        for cell in cells_to_add:
            try:
                self.world.add_cell(cell)
            except ValueError:
                pass
