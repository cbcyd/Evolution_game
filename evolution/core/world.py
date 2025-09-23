from typing import Dict, Tuple, Iterable
from evolution.core.cell import Cell

class World:
    """
    Represents the 2D world where cells live.

    Attributes:
        width (int): The width of the world.
        height (int): The height of the world.
        _cells (Dict[Tuple[int, int], Cell]): A dictionary mapping coordinates to cells.
    """

    def __init__(self, width: int, height: int):
        """
        Initializes the world.

        Args:
            width (int): The width of the world.
            height (int): The height of the world.
        """
        self.width = width
        self.height = height
        self._cells: Dict[Tuple[int, int], Cell] = {}

    def add_cell(self, cell: Cell):
        """
        Adds a cell to the world.

        Args:
            cell (Cell): The cell to add.

        Raises:
            ValueError: If the cell's position is out of bounds.
        """
        if not (0 <= cell.x < self.width and 0 <= cell.y < self.height):
            raise ValueError("Cell position is out of world bounds.")
        self._cells[(cell.x, cell.y)] = cell

    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Returns the cell at a given position.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            Cell | None: The cell at the given position, or None if empty.
        """
        return self._cells.get((x, y))

    def remove_cell(self, cell: Cell):
        """
        Removes a cell from the world.

        Args:
            cell (Cell): The cell to remove.
        """
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
