import atexit
import functools
import logging
import os
import sys
from math import log10

import torch
from termcolor import colored

from core.meter.meters import AverageMeter


@functools.lru_cache(maxsize=None)
def _cached_log_stream(filename):
    # use 1K buffer if writing to cloud storage
    io = os.open(filename, "a", buffering=1024 if "://" in filename else -1)
    atexit.register(io.close)
    return io


def _current_total_formatter(current, total):
    width = int(log10(total)) + 1
    return ("[{:" + str(width) + "}/{:" + str(width) + "}]").format(current, total)


def iteration(logger, summary, phase, global_step, epoch, num_epochs, step, num_steps, values, multiple_lines=False):

    # Build message and write summary
    msg = _current_total_formatter(
        epoch, num_epochs) + " " + _current_total_formatter(step, num_steps)
    for k, v in values.items():
        if isinstance(v, AverageMeter):
            msg += "\n" if multiple_lines else "" + \
                "\t{}={:.3f} ({:.3f})".format(k, v.value.item(), v.mean.item())
            if summary is not None:
                summary.add_scalar("{}/{}".format(phase, k),
                                   v.value.item(), global_step)
        else:
            msg += "\n" if multiple_lines else "" + "\t{}={:.3f}".format(k, v)
            if summary is not None:
                summary.add_scalar("{}/{}".format(phase, k), v, global_step)

    # Write log
    logger.info(msg)


def _log_api_usage(identifier: str):
    """
    Internal function used to log the usage of different visloc components
    inside facebook's infra.
    """
    torch._C._log_api_usage_once("visloc." + identifier)


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
