import functools
import logging
import os
import sys

from termcolor import colored


class _ColorfulFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self._root_name = kwargs.pop("root_name") + "."
        self._abbrev_name = kwargs.pop("abbrev_name", "")
        if len(self._abbrev_name):
            self._abbrev_name = self._abbrev_name + "."
        super(_ColorfulFormatter, self).__init__(*args, **kwargs)

    def formatMessage(self, record):
        record.name = record.name.replace(self._root_name, self._abbrev_name)
        log = super(_ColorfulFormatter, self).formatMessage(record)
        if record.levelno == logging.WARNING:
            prefix = colored("WARNING", "red", attrs=["blink"])
        elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            prefix = colored("ERROR", "red", attrs=["blink", "underline"])
        else:
            return log
        return prefix + " " + log


@functools.lru_cache()
def init_logger(log_file=None, *, color=True, name="visloc", abbrev_name=None, file_name=None):
    """
    Initialize logger and set its verbosity level to "DEBUG".
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # formaters
    plain_formatter = logging.Formatter(
        "[%(asctime)s %(name)s]: %(message)s", datefmt="%m/%d %H:%M")
    color_formatter = _ColorfulFormatter(
        colored("[%(asctime)s %(name)s]: ", "green") + "%(message)s",
        datefmt="%m/%d %H:%M",
        root_name=name,
        abbrev_name=str(abbrev_name),)

    # console logging
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(color_formatter if color else plain_formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # file logging
    if log_file is not None:
        if file_name is not None:
            filename = os.path.join(log_file, file_name + ".txt")
        else:
            filename = os.path.join(log_file, "log.txt")

        file_handler = logging.FileHandler(filename, mode="w")
        file_handler.setFormatter(plain_formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    return logger
