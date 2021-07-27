from typing import Tuple, Union

import numpy as np


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
    return cube_tetra((x0, y0, z0), (x1, y1, z1), (nx, ny, nz))


def cube_hexa(
    a0: Tuple[float, float, float],
    a1: Tuple[float, float, float],
    n: Union[int, Tuple[int, int, int]],
):
    if isinstance(n, tuple):
        nx, ny, nz = n
    else:
        nx = n
        ny = n
        nz = n

    nx1 = nx + 1
    ny1 = ny + 1
    nz1 = nz + 1

    xmin, ymin, zmin = a0
    xmax, ymax, zmax = a1

    # Generate suitable ranges for parametrization
    x_range = np.linspace(xmin, xmax, nx1)
    y_range = np.linspace(ymin, ymax, ny1)
    z_range = np.linspace(zmin, zmax, nz1)

    # Create the vertices.
    x, y, z = np.meshgrid(x_range, y_range, z_range, indexing="ij")
    # Alternative with slightly different order:
    # ```
    # points = np.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    points = np.array([x, y, z]).T.reshape(-1, 3)

    # Create the elements (cells).
    a0 = np.add.outer(np.arange(nx), nx1 * np.arange(ny))
    a = np.add.outer(a0, nx1 * ny1 * np.arange(nz))
    elems = np.concatenate(
        [
            a[..., None],
            a[..., None] + 1,
            a[..., None] + nx1 + 1,
            a[..., None] + nx1,
            #
            a[..., None] + nx1 * ny1,
            a[..., None] + nx1 * ny1 + 1,
            a[..., None] + nx1 * ny1 + nx1 + 1,
            a[..., None] + nx1 * ny1 + nx1,
        ],
        axis=3,
    ).reshape(-1, 8)

    return points, elems


def cube_tetra(
    a0: Tuple[float, float, float],
    a1: Tuple[float, float, float],
    n: Union[int, Tuple[int, int, int]],
):
    if isinstance(n, tuple):
        nx, ny, nz = n
    else:
        nx = n
        ny = n
        nz = n

    nx1 = nx + 1
    ny1 = ny + 1
    nz1 = nz + 1

    xmin, ymin, zmin = a0
    xmax, ymax, zmax = a1

    # Generate suitable ranges for parametrization
    x_range = np.linspace(xmin, xmax, nx1)
    y_range = np.linspace(ymin, ymax, ny1)
    z_range = np.linspace(zmin, zmax, nz1)

    # Create the vertices.
    x, y, z = np.meshgrid(x_range, y_range, z_range, indexing="ij")
    # Alternative with slightly different order:
    # ```
    # points = np.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    points = np.array([x, y, z]).T.reshape(-1, 3)

    # Create the elements (cells).
    a = np.arange(len(points)).reshape(nx1, ny1, nz1)
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
    idx = np.ones((nx, ny, nz), dtype=bool)
    idx[::2, 1::2, ::2] = False
    idx[::2, ::2, 1::2] = False
    idx[1::2, ::2, ::2] = False
    idx[1::2, 1::2, 1::2] = False

    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See
    # <http://www.baumanneduard.ch/Splitting%20a%20cube%20in%20tetrahedras2.htm>
    # Also interesting: <http://en.wikipedia.org/wiki/Marching_tetrahedrons>.
    cells = [
        # regular; make sure the order of the points is such that the signed volume is
        # positive
        [c[0][idx], c[1][idx], c[4][idx], c[3][idx]],
        [c[1][idx], c[2][idx], c[6][idx], c[3][idx]],
        [c[1][idx], c[3][idx], c[6][idx], c[4][idx]],
        [c[1][idx], c[4][idx], c[6][idx], c[5][idx]],
        [c[3][idx], c[4][idx], c[7][idx], c[6][idx]],
        # the rest rotated such that it fits with the others; basically we change
        # "bottom" and "top" of the dice
        [c[4][~idx], c[5][~idx], c[7][~idx], c[0][~idx]],
        [c[5][~idx], c[6][~idx], c[7][~idx], c[2][~idx]],
        [c[5][~idx], c[7][~idx], c[0][~idx], c[2][~idx]],
        [c[5][~idx], c[0][~idx], c[1][~idx], c[2][~idx]],
        [c[7][~idx], c[0][~idx], c[2][~idx], c[3][~idx]],
    ]

    cells = np.column_stack([np.array(c).reshape(4, -1) for c in cells]).T

    return points, cells
