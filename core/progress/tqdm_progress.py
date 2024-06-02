from tqdm import tqdm
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn


def tqdm_progress_bar(iterable, desc="Progress", total=None, colour="white"):
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    return tqdm(iterable, desc=desc, total=total, colour=colour)


def rich_progress_bar(iterable, desc="Progress", total=None, color="white"):
    progress = Progress(
        TextColumn(f"[bold {color}]{desc}"),
        BarColumn(bar_width=None, style=color),
        "[progress.percentage]{task.percentage:>3.1f}%",
        TimeRemainingColumn(),
        expand=True
    )

    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    task_id = progress.add_task(desc, total=total)

    def progress_generator():
        with progress:
            for item in iterable:
                yield item
                progress.update(task_id, advance=1)

    return progress_generator()
