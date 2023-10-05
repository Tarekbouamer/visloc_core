

from tqdm import tqdm


def tqdm_progress(iterable, desc=None, total=None, colour="white", smoothing=1.0, bar_format=None):
    """write universal tqrdm progress bar and return the progress bar object    
    """

    if not desc:
        desc = "progress"
    if not total:
        total = len(iterable)
    if not bar_format:
        bar_format = "{desc}: {percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"

    progress_bar = tqdm(
        iterable=iterable,
        desc=desc,
        total=total,
        colour=colour,
        smoothing=smoothing,
        bar_format=bar_format,
    )

    return progress_bar
