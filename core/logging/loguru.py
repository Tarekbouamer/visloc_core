import os
import sys

from loguru import logger


def init_loguru(name="VisLoc", log_file=None, file_name=None):

    # log file
    if file_name:
        log_file = os.path.join(log_file, file_name + ".log")

    logger_format = (
        "<g>{time:YYYY-MM-DD HH:mm}</g>|"
        f"<m>{name}</m>|"
        "<level>{level: <8}</level>|"
        "<c>{function}</c>:<c>{line}</c>|"
        "{extra[ip]} {extra[user]} <level>{message}</level>")

    # ip and user
    logger.configure(extra={"ip": "", "user": ""})  # Default values

    # Remove the default logger configuration
    logger.remove()
    logger.add(log_file, enqueue=True) 

    # You can add additional sinks for logging, such as console output
    logger.add(sys.stderr, format=logger_format, colorize=True)

    logger.success("init logger")

    return logger
