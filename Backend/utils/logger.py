# utils/logger.py
import logging


def setup_logger(name: str):
    """Set up a logger with a specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of logs

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Ensure console handler captures DEBUG level logs

    # Create formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(ch)

    return logger
