import logging
import os
from datetime import datetime as dt
from functools import lru_cache
from logging.handlers import RotatingFileHandler

from app.core.settings import settings

os.makedirs(settings.LOGS_DIR, exist_ok=True)
now_str = dt.now().strftime("%Y%m%dT%H%M%S.%Z")
logger_file_name = f"{settings.LOGS_DIR}/am1-backend-{now_str}.log"


# Singleton Logger Function
@lru_cache(maxsize=1)
def get_logger(name=".am1_app.log"):
    """Returns a singleton logger instance that logs to both console and file."""
    logger = logging.getLogger(name)

    # If the logger already exists, return it
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)  # Set logging level (DEBUG, INFO, ERROR, etc.)

    # Format for log messages
    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] [%(filename)s:%(lineno)d] [Thread-%(thread)d]: %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # File Handler (Rotating)
    file_handler = RotatingFileHandler(
        settings.LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger
