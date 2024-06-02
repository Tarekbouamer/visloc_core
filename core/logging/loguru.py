from datetime import datetime
from loguru import logger
from pathlib import Path
import sys

def get_current_time_as_string():
    """Returns the current time formatted as a string suitable for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def init_loguru(name="app", log_dir=None):
    """
    Initialize and configure the Loguru logger with automatic file naming based on the current time.

    Parameters:
    - name (str): Name of the application or logger.
    - log_dir (str or Path): Directory path for log files.

    Returns:
    - logger: Configured logger instance.
    """
    if log_dir:
        log_dir = Path(log_dir)  # Convert log_dir to a Path object if it's not already one
        log_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
        file_name = f"{get_current_time_as_string()}.log"
        log_file = log_dir / file_name
    else:
        log_file = None  # Disable file logging if directory is not specified

    logger_format = (
        "<g>{time:YYYY-MM-DD HH:mm}</g>|"
        f"<m>{name}</m>|"
        "<level>{level: <8}</level>|"
        "<c>{function}</c>:<c>{line}</c>|"
        "{extra[ip]} {extra[user]} <level>{message}</level>")

    logger.configure(extra={"ip": "N/A", "user": "N/A"})
    logger.remove()  # Clear existing configurations
    if log_file:
        logger.add(str(log_file), enqueue=True)  # Add file sink
    logger.add(sys.stderr, format=logger_format, colorize=True)  # Add console sink

    logger.success("Logger initialized with file: " + (str(file_name) if log_dir else "No file logging"))
    return logger
