from typing import Dict, Tuple, Iterable
from evolution.core.cell import Cell

class World:
    """Represents the 2D world where cells live."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._cells: Dict[Tuple[int, int], Cell] = {}

    def add_cell(self, cell: Cell):
        """Adds a cell to the world."""
        if not (0 <= cell.x < self.width and 0 <= cell.y < self.height):
            raise ValueError("Cell position is out of world bounds.")
        self._cells[(cell.x, cell.y)] = cell

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Returns the cell at a given position, or None if empty."""
        return self._cells.get((x, y))

    def remove_cell(self, cell: Cell):
        """Removes a cell from the world."""
        if (cell.x, cell.y) in self._cells:
            # Make sure we are removing the exact same cell object
            if self._cells[(cell.x, cell.y)] is cell:
                del self._cells[(cell.x, cell.y)]

    @property
    def cells(self) -> Iterable[Cell]:
        """Returns an iterator over all cells in the world."""
        return self._cells.values()

    @cells.setter
    def cells(self, cells: Dict[Tuple[int, int], Cell]):
        """Replaces all cells in the world."""
        self._cells = cells
