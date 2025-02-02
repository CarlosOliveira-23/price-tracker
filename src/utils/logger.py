import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)


def log_info(message):
    """Logs an info message."""
    logging.info(message)


def log_error(message):
    """Logs an error message."""
    logging.error(message)


def log_warning(message):
    """Logs a warning message."""
    logging.warning(message)
