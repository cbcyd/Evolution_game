import pickle
import os
import logging
from pathlib import Path
from evolution.core.world import World

def save_world(world: World, filepath: str | Path):
    """Saves the world state to a file using pickle and an atomic write."""
    filepath = Path(filepath)
    temp_filepath = filepath.with_suffix(filepath.suffix + ".tmp")
    try:
        with open(temp_filepath, "wb") as f:
            pickle.dump(world, f)
        os.replace(temp_filepath, filepath)
        logging.info(f"World saved successfully to {filepath}")
    except Exception as e:
        logging.error(f"Error saving world to {filepath}: {e}")

def load_world(filepath: str | Path) -> World | None:
    """Loads the world state from a file."""
    filepath = Path(filepath)
    if not os.path.exists(filepath):
        logging.warning(f"No save file found at {filepath}.")
        return None

    try:
        with open(filepath, "rb") as f:
            world = pickle.load(f)
        logging.info(f"World loaded successfully from {filepath}")
        return world
    except Exception as e:
        logging.error(f"Error loading world from {filepath}: {e}")
        return None
