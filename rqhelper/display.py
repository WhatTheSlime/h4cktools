import coloredlogs
import verboselogs
import logging
import sys
import os
from datetime import datetime


def init_logger(name, logs_folder_path, debug=False, verbose=False):
    """Initialization of coloredlogs.

    Parameters:
        name: Default name will be print on the log.
        logs_folder_path: Path to folder where logs will be stored.
        debug: Enable debugs and verboses logs.
        verbose: Enable verboses logs.
    """

    # Setup logs file.
    filename = os.path.join(
        logs_folder_path, f"{name.lower()}.log"
    )
    logging.basicConfig(filename=filename, filemode="w")

    # Logs format.
    coloredlogs.DEFAULT_LOG_FORMAT = (
        "%(asctime)s %(name)s %(levelname)s %(message)s"
    )

    # Changing field colors.
    coloredlogs.DEFAULT_FIELD_STYLES = {
        "asctime": {"color": "white"},
        "name": {"color": "white"},
        "levelname": {"color": "white", "bold": True},
        "programname": {"color": "white"},
    }

    # Changing level colors.
    coloredlogs.DEFAULT_LEVEL_STYLES = {
        "critical": {"color": "red", "bold": True},
        "debug": {"color": "white", "faint": True},
        "error": {"color": "red"},
        "info": {"color": "white"},
        "notice": {"color": "green"},
        "spam": {"color": "green", "faint": True},
        "success": {"color": "green", "bold": True},
        "verbose": {"color": "blue"},
        "warning": {"color": "yellow"},
    }

    verboselogs.install()

    coloredlogs.install(level="INFO")

    if verbose:
        coloredlogs.install(level="VERBOSE")

    if debug:
        coloredlogs.install(level="DEBUG")

    return logging.getLogger(name)


def display_progress(
    iteration,
    total,
    prefix="Progress:",
    suffix="Completed",
    decimals=1,
    length=50,
    fill="\033[34m▓\033[0m",
    percent_format=False,
):
    """Call in a loop to create terminal progress bar

    Parameters:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent 
                                  complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    filledLength = int(length * iteration // total)
    bar = (fill * filledLength) + "-" * (length - filledLength)
    indicator = f"{iteration}/{total}"
    if percent_format:
        indicator = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        ) + "%"

    clear_line()
    print(f"\r{prefix} │{bar}│ {indicator} {suffix}", end="\r")
    # Print New Line on Complete
    if iteration >= total:
        clear_line()

def clear_line():
    print("\r" + " " * os.get_terminal_size().columns, end="\r")
