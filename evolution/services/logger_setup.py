import logging

def setup_logging():
    """Sets up logging to a file and the console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s",
        handlers=[
            logging.FileHandler("evolution.log", mode='w'),
            logging.StreamHandler()
        ]
    )
