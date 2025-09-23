import time
import neat
from PySide6.QtCore import QObject, Signal

from evolution.core.world import World
from evolution.core.cell import Cell
from evolution.engine.loop import Simulation
from evolution.behaviors.strategies import neat_strategy

class SimulationWorker(QObject):
    """
    A worker object that runs the simulation in a separate thread.
    Can run in 'simple' mode (continuous simulation) or 'neat' mode (generation-based).
    """
    world_updated = Signal(object)
    stats_updated = Signal(dict)
    finished = Signal()

    def __init__(self, simulation: Simulation, neat_pop: neat.Population = None, neat_config=None):
        super().__init__()
        self.simulation = simulation
        self.neat_pop = neat_pop
        self.neat_config = neat_config
        self.mode = 'simple' if neat_pop is None else 'neat'

        self._running = False
        self._paused = True

    def run(self):
        """The main simulation loop."""
        self._running = True
        self._paused = False

        while self._running:
            if not self._paused:
                if self.mode == 'simple':
                    self.simulation.step()
                    self.world_updated.emit(self.simulation.world)
                    time.sleep(0.1)
                elif self.mode == 'neat':
                    self.run_neat_generation()
            else:
                time.sleep(0.1)

        self.finished.emit()

    def run_neat_generation(self):
        """Runs a single generation of the NEAT algorithm."""
        if self.neat_pop is None:
            return

        # Use NEAT's StdOutReporter to capture stats without printing
        # In a future step, we'll create a custom reporter to emit signals
        self.neat_pop.reporters.start_generation(self.neat_pop.generation)

        # Evaluate all genomes
        self.eval_genomes(self.neat_pop.population.items(), self.neat_config)

        # Gather and report statistics
        best = None
        for g in self.neat_pop.population.values():
            if best is None or g.fitness > best.fitness:
                best = g
        self.neat_pop.reporters.post_evaluate(self.neat_config, self.neat_pop.population, self.neat_pop.species, best)

        # Create the next generation
        self.neat_pop.population = self.neat_pop.reproduction.reproduce(
            self.neat_config, self.neat_pop.species, self.neat_config.pop_size, self.neat_pop.generation
        )

        # Check for extinction
        if not self.neat_pop.species.species:
            print("Extinction!")
            self.stop()
            return

        # Speciate the new population
        self.neat_pop.species.speciate(self.neat_config, self.neat_pop.population, self.neat_pop.generation)
        self.neat_pop.reporters.end_generation(self.neat_config, self.neat_pop.population, self.neat_pop.species)

        # Emit stats (simplified for now)
        stats = {
            "generation": self.neat_pop.generation,
            "best_fitness": best.fitness if best else 0,
            "num_species": len(self.neat_pop.species.species),
        }
        self.stats_updated.emit(stats)

        self.neat_pop.generation += 1

    def eval_genomes(self, genomes, config):
        """Evaluate the fitness of each genome in the population."""
        for genome_id, genome in genomes:
            # Create a new world and simulation for each genome evaluation
            world = World(width=40, height=30)
            cell = Cell(energy=10.0, x=20, y=15, strategy=neat_strategy, genome=genome)
            world.add_cell(cell)

            # The simulation runs for a fixed number of ticks
            sim = Simulation(world, self.simulation.event_bus, config)
            for _ in range(100): # 100 ticks per evaluation
                sim.step()

            genome.fitness = cell.energy if cell.is_alive else 0.0

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def stop(self):
        self._running = False

    def step(self):
        """Performs a single step, depending on the mode."""
        if self._paused:
            if self.mode == 'simple':
                self.simulation.step()
                self.world_updated.emit(self.simulation.world)
            elif self.mode == 'neat':
                self.run_neat_generation()
