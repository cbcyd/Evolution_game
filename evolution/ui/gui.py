import sys
import neat
from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
)

from evolution.core.world import World
from evolution.core.cell import Cell
from evolution.engine.loop import Simulation
from evolution.services.event_bus import EventBus
from evolution.services import persistence
from evolution.ui.world_view import WorldView
from evolution.ui.simulation_worker import SimulationWorker
from evolution.behaviors.strategies import random_walk_strategy

class EvolutionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Evolution Simulation")
        self.setGeometry(100, 100, 1000, 800)

        # --- Main Layout ---
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # --- NEAT Config ---
        config_path = "neat.cfg"
        self.neat_config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                       neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                       config_path)

        # --- Simulation and World Setup ---
        # The world is now mainly a display buffer; the NEAT sims happen in memory
        self.world = World(width=40, height=30)
        self.event_bus = EventBus()
        # This simulation object is a placeholder for the simple simulation mode
        self.simulation = Simulation(self.world, self.event_bus, self.neat_config)

        # --- NEAT Population ---
        self.neat_pop = neat.Population(self.neat_config)
        self.neat_pop.add_reporter(neat.StdOutReporter(True)) # For console stats

        # --- WorldView ---
        self.world_view = WorldView(self.world)
        main_layout.addWidget(self.world_view, stretch=4)

        # --- Controls ---
        self.setup_controls(main_layout)

        # --- Simulation Thread ---
        self.setup_simulation_thread()

    def setup_controls(self, parent_layout):
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        parent_layout.addWidget(controls_widget, stretch=1)

        self.start_button = QPushButton("Start Evolution")
        self.start_button.setToolTip("Start or resume the NEAT evolution.")

        self.pause_button = QPushButton("Pause Evolution")
        self.pause_button.setToolTip("Pause the NEAT evolution.")

        self.step_button = QPushButton("Step Generation")
        self.step_button.setToolTip("Run a single NEAT generation.")

        self.save_button = QPushButton("Save Population")
        self.load_button = QPushButton("Load Population")

        self.pause_button.setEnabled(False)

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.step_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.save_button)
        controls_layout.addWidget(self.load_button)

        self.start_button.clicked.connect(self.on_start)
        self.pause_button.clicked.connect(self.on_pause)
        self.step_button.clicked.connect(self.on_step)
        self.save_button.clicked.connect(self.on_save)
        self.load_button.clicked.connect(self.on_load)

    def setup_simulation_thread(self):
        self.thread = QThread()
        # The worker is now created in NEAT mode
        self.worker = SimulationWorker(self.simulation, self.neat_pop, self.neat_config)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.world_updated.connect(self.update_world_view)
        self.worker.stats_updated.connect(self.on_stats_updated)

    def on_stats_updated(self, stats):
        # In a future step, this will update GUI labels
        print(f"Stats received: {stats}")

    def on_start(self):
        if not self.thread.isRunning():
            self.thread.start()
        self.worker.resume()
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.step_button.setEnabled(False)
        self.load_button.setEnabled(False) # Can't load while running

    def on_pause(self):
        self.worker.pause()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.step_button.setEnabled(True)
        self.load_button.setEnabled(True) # Can load while paused

    def on_step(self):
        self.worker.step()

    def on_save(self):
        # Pause the simulation to ensure a consistent state is saved
        was_running = self.thread.isRunning() and not self.worker._paused
        if was_running:
            self.on_pause()

        filepath, _ = QFileDialog.getSaveFileName(self, "Save World", "", "Evolution Save Files (*.pkl)")
        if filepath:
            persistence.save_world(self.simulation.world, filepath)

        # Resume if it was running before
        if was_running:
            self.on_start()

    def on_load(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load World", "", "Evolution Save Files (*.pkl)")
        if filepath:
            loaded_world = persistence.load_world(filepath)
            if loaded_world:
                # Replace the world in the simulation and update the view
                self.simulation.world = loaded_world
                self.world_view.set_world(loaded_world)

    def update_world_view(self, world):
        self.world_view.set_world(world)

    def closeEvent(self, event):
        """Ensure the simulation thread is stopped when closing the window."""
        if self.thread.isRunning():
            self.worker.stop()
            self.thread.quit()
            self.thread.wait() # Wait for the thread to finish
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EvolutionGUI()
    window.show()
    sys.exit(app.exec())
