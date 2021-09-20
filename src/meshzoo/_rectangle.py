from typing import Tuple, Union

import numpy as np


# backwards compatibility
def rectangle(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    nx: int,
    ny: int,
):
    return rectangle_tri((x0, y0), (x1, y1), (nx, ny))


def rectangle_quad(
    a0: Tuple[float, float],
    a1: Tuple[float, float],
    n: Union[int, Tuple[int, int]],
):
    nx, ny = (n, n) if isinstance(n, int) else n

    xmin, ymin = a0
    xmax, ymax = a1

    x_range = np.linspace(xmin, xmax, nx + 1)
    y_range = np.linspace(ymin, ymax, ny + 1)
    nodes = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T

    a = np.add.outer(np.arange(nx), nx * np.arange(ny)) + np.arange(ny)
    elems = np.array([a, a + 1, a + nx + 2, a + nx + 1]).reshape(4, -1).T
    return nodes, elems


def rectangle_tri(
    a0: Tuple[float, float],
    a1: Tuple[float, float],
    n: Union[int, Tuple[int, int]],
    variant: str = "zigzag",
):
    nx, ny = (n, n) if isinstance(n, int) else n

    # Create the vertices.
    x_range = np.linspace(a0[0], a1[0], nx + 1)
    y_range = np.linspace(a0[1], a1[1], ny + 1)
    nodes = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T

    a = np.add.outer(np.arange(nx + 1), (nx + 1) * np.arange(ny + 1))

    # indices of corners
    #
    # c[3]   c[2]
    #    _____
    #    |   |
    #    |___|
    #
    # c[0]   c[1]
    #
    c = [
        a[:-1, :-1],
        a[1:, :-1],
        a[1:, 1:],
        a[:-1, 1:],
    ]

    if variant == "up":
        cells = [
            [c[0], c[1], c[2]],
            [c[0], c[2], c[3]],
        ]
    elif variant == "down":
        cells = [
            [c[0], c[1], c[3]],
            [c[1], c[2], c[3]],
        ]
    elif variant == "zigzag":
        # https://stackoverflow.com/a/68550456/353337
        idx = np.ones((nx, ny), dtype=bool)
        idx[1::2, ::2] = False
        idx[::2, 1::2] = False
        cells = [
            # up
            [c[0][idx], c[1][idx], c[2][idx]],
            [c[0][idx], c[2][idx], c[3][idx]],
            # down
            [c[0][~idx], c[1][~idx], c[3][~idx]],
            [c[1][~idx], c[2][~idx], c[3][~idx]],
        ]
    else:
        assert variant == "center"
        i = np.arange(nx)
        j = np.arange(ny)
        i, j = np.meshgrid(i, j, indexing="ij")

        idx = np.ones(n, dtype=bool)
        idx[(i < nx // 2) & (j < ny // 2)] = False
        idx[(i >= nx // 2) & (j >= ny // 2)] = False
        cells = [
            # up
            [c[0][idx], c[1][idx], c[2][idx]],
            [c[0][idx], c[2][idx], c[3][idx]],
            # down
            [c[0][~idx], c[1][~idx], c[3][~idx]],
            [c[1][~idx], c[2][~idx], c[3][~idx]],
        ]

    cells = np.column_stack([np.array(c).reshape(3, -1) for c in cells]).T

    return nodes, cells
