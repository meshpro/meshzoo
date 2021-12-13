from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


# backwards compatibility
def cube(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    z0: float,
    z1: float,
    nx: int,
    ny: int,
    nz: int,
):
    return cube_tetra(
        np.linspace(x0, x1, nx + 1),
        np.linspace(y0, y1, ny + 1),
        np.linspace(z0, z1, nz + 1),
    )


def cube_hexa(
    x_range: ArrayLike, y_range: ArrayLike, z_range: ArrayLike
) -> tuple[np.ndarray, np.ndarray]:
    x_range = np.asarray(x_range)
    y_range = np.asarray(y_range)
    z_range = np.asarray(z_range)

    nx1 = len(x_range)
    ny1 = len(y_range)
    nz1 = len(z_range)

    # Create the vertices.
    x, y, z = np.meshgrid(x_range, y_range, z_range, indexing="ij")

    # Alternative with slightly different order:
    # ```
    # points = np.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    points = np.array([x, y, z]).T.reshape(-1, 3)

    # Create the cells.
    a = np.arange(len(points)).reshape(nz1, ny1, nx1)
    a = np.transpose(a, [2, 1, 0])

    # `c` contains the indices of each "cube" like
    #
    #
    #          c[7]     c[6]
    #            ________
    #           /       /|
    #     c[4] /_______/ | c[5]
    #         |        | |
    #         |        | |
    #         |        | / c[2]
    #         |________|/
    #
    #       c[0]      c[1]
    #
    cells = (
        np.array(
            [
                a[:-1, :-1, :-1],
                a[1:, :-1, :-1],
                a[1:, 1:, :-1],
                a[:-1, 1:, :-1],
                a[:-1, :-1, 1:],
                a[1:, :-1, 1:],
                a[1:, 1:, 1:],
                a[:-1, 1:, 1:],
            ]
        )
        .reshape(8, -1)
        .T
    )

    return points, cells


def cube_tetra(x_range: ArrayLike, y_range: ArrayLike, z_range: ArrayLike):
    x_range = np.asarray(x_range)
    y_range = np.asarray(y_range)
    z_range = np.asarray(z_range)

    nx1 = len(x_range)
    ny1 = len(y_range)
    nz1 = len(z_range)

    # Create the vertices.
    x, y, z = np.meshgrid(x_range, y_range, z_range, indexing="ij")
    # Alternative with slightly different order:
    # ```
    # points = np.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    points = np.array([x, y, z]).T.reshape(-1, 3)

    # Create the elements (cells).
    a = np.arange(len(points)).reshape(nz1, ny1, nx1)
    a = np.transpose(a, [2, 1, 0])

    #
    # `c` contains the indices of each "cube" like
    #
    #
    #          c[7]     c[6]
    #            ________
    #           /       /|
    #     c[4] /_______/ | c[5]
    #         |        | |
    #         |        | |
    #         |        | / c[2]
    #         |________|/
    #
    #       c[0]      c[1]
    #
    c = [
        a[:-1, :-1, :-1],
        a[1:, :-1, :-1],
        a[1:, 1:, :-1],
        a[:-1, 1:, :-1],
        a[:-1, :-1, 1:],
        a[1:, :-1, 1:],
        a[1:, 1:, 1:],
        a[:-1, 1:, 1:],
    ]

    # 3D checkers
    idx = np.ones((nx1 - 1, ny1 - 1, nz1 - 1), dtype=bool)
    idx[::2, 1::2, ::2] = False
    idx[::2, ::2, 1::2] = False
    idx[1::2, ::2, ::2] = False
    idx[1::2, 1::2, 1::2] = False

    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See
    # <http://www.baumanneduard.ch/Splitting%20a%20cube%20in%20tetrahedras2.htm>
    # Also interesting: <https://en.wikipedia.org/wiki/Marching_tetrahedrons>.
    cells = [
        # regular; make sure the order of the points is such that the signed volume is
        # positive
        [c[0][idx], c[1][idx], c[3][idx], c[4][idx]],
        [c[1][idx], c[2][idx], c[3][idx], c[6][idx]],
        [c[1][idx], c[3][idx], c[4][idx], c[6][idx]],
        [c[1][idx], c[4][idx], c[5][idx], c[6][idx]],
        [c[3][idx], c[4][idx], c[6][idx], c[7][idx]],
        # the rest rotated such that it fits with the others; basically we change
        # "bottom" and "top" of the dice
        [c[4][~idx], c[5][~idx], c[0][~idx], c[7][~idx]],
        [c[5][~idx], c[6][~idx], c[2][~idx], c[7][~idx]],
        [c[5][~idx], c[7][~idx], c[2][~idx], c[0][~idx]],
        [c[5][~idx], c[0][~idx], c[2][~idx], c[1][~idx]],
        [c[7][~idx], c[0][~idx], c[3][~idx], c[2][~idx]],
    ]

    cells = np.column_stack([np.array(c).reshape(4, -1) for c in cells]).T

    return points, cells
