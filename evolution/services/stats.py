class Stats:
    """A simple class to hold statistics for a simulation run."""
    def __init__(self):
        self.births = 0
        self.deaths = 0

    def record_birth(self):
        """Records a cell division event."""
        self.births += 1

    def record_death(self):
        """Records a cell death event."""
        self.deaths += 1

    def report(self) -> str:
        """Returns a string report of the statistics."""
        return f"Births: {self.births}, Deaths: {self.deaths}"
