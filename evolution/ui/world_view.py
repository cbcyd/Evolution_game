from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

from evolution.core.world import World

class WorldView(QWidget):
    def __init__(self, world: World, parent=None):
        super().__init__(parent)
        self.world = world
        self.cell_size = 20  # Size of each cell in pixels

    def set_world(self, world: World):
        """Updates the world and triggers a repaint."""
        self.world = world
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Clear the background
        painter.fillRect(self.rect(), QColor("black"))

        # Draw grid
        painter.setPen(QColor("gray"))
        for x in range(0, self.width(), self.cell_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), self.cell_size):
            painter.drawLine(0, y, self.width(), y)

        # Draw cells
        for cell in self.world.cells:
            # For now, a simple representation
            color = QColor(Qt.GlobalColor.green)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                cell.x * self.cell_size,
                cell.y * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
