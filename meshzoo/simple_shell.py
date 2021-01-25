import numpy as np


def simple_shell():
    nodes = np.array(
        [
            [+0.0, +0.0, 1.0],
            [+1.0, +0.0, 0.0],
            [+0.0, +1.0, 0.0],
            [-1.0, +0.0, 0.0],
            [+0.0, -1.0, 0.0],
        ]
    )
    elems = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1]])
    return nodes, elems
