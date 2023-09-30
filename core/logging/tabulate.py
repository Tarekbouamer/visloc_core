
import numpy as np
from tabulate import tabulate


def create_small_table(small_dict, fmt=".3f"):
    """
    """
    keys, values = tuple(zip(*small_dict.items()))

    #
    vv = []
    for v in values:
        if isinstance(v, np.ndarray):
            # flatten
            v = v.reshape(-1).tolist()
            v = np.array(v)
        vv.append(v)

    table = tabulate(
        [vv],
        headers=keys,
        tablefmt="pipe",
        floatfmt=fmt,
        stralign="center",
        numalign="center",
    )

    return table
