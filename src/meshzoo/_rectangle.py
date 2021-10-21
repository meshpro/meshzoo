from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


# backwards compatibility
def rectangle(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    nx: int,
    ny: int,
):
    x_range = np.linspace(x0, x1, nx + 1)
    y_range = np.linspace(y0, y1, ny + 1)
    return rectangle_tri(x_range, y_range)


def rectangle_quad(x_range: ArrayLike, y_range: ArrayLike, cell_type: str = "quad4"):
    x_range = np.asarray(x_range)
    y_range = np.asarray(y_range)

    nx = len(x_range)
    ny = len(y_range)

    if cell_type == "quad4":
        points = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T
        a = np.arange(nx * ny).reshape(ny, nx).T

        cells = (
            np.array([a[:-1, :-1], a[1:, :-1], a[1:, 1:], a[:-1, 1:]]).reshape(4, -1).T
        )
    elif cell_type == "quad8":
        k = 0
        points_corner = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T
        a_corner = np.arange(nx * ny).reshape(ny, nx).T
        k += a_corner.size

        x_mid = (x_range[:-1] + x_range[1:]) / 2
        points_xmid = np.array(np.meshgrid(x_mid, y_range)).reshape(2, -1).T
        a_xmid = k + np.arange((nx - 1) * ny).reshape(ny, nx - 1).T
        k += a_xmid.size

        y_mid = (y_range[:-1] + y_range[1:]) / 2
        points_ymid = np.array(np.meshgrid(x_range, y_mid)).reshape(2, -1).T
        a_ymid = k + np.arange(nx * (ny - 1)).reshape(ny - 1, nx).T

        points = np.row_stack([points_corner, points_xmid, points_ymid])

        cells = (
            np.array(
                [
                    a_corner[:-1, :-1],
                    a_corner[1:, :-1],
                    a_corner[1:, 1:],
                    a_corner[:-1, 1:],
                    a_xmid[:, :-1],
                    a_ymid[1:, :],
                    a_xmid[:, 1:],
                    a_ymid[:-1, :],
                ]
            )
            .reshape(8, -1)
            .T
        )
    else:
        assert cell_type == "quad9"
        k = 0
        points_corner = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T
        a_corner = np.arange(nx * ny).reshape(ny, nx).T
        k += a_corner.size

        x_mid = (x_range[:-1] + x_range[1:]) / 2
        points_xmid = np.array(np.meshgrid(x_mid, y_range)).reshape(2, -1).T
        a_xmid = k + np.arange((nx - 1) * ny).reshape(ny, nx - 1).T
        k += a_xmid.size

        y_mid = (y_range[:-1] + y_range[1:]) / 2
        points_ymid = np.array(np.meshgrid(x_range, y_mid)).reshape(2, -1).T
        a_ymid = k + np.arange(nx * (ny - 1)).reshape(ny - 1, nx).T
        k += a_ymid.size

        points_center = np.array(np.meshgrid(x_mid, y_mid)).reshape(2, -1).T
        a_center = k + np.arange((nx - 1) * (ny - 1)).reshape(ny - 1, nx - 1).T

        points = np.row_stack([points_corner, points_xmid, points_ymid, points_center])

        cells = (
            np.array(
                [
                    a_corner[:-1, :-1],
                    a_corner[1:, :-1],
                    a_corner[1:, 1:],
                    a_corner[:-1, 1:],
                    a_xmid[:, :-1],
                    a_ymid[1:, :],
                    a_xmid[:, 1:],
                    a_ymid[:-1, :],
                    a_center,
                ]
            )
            .reshape(9, -1)
            .T
        )

    return points, cells


def rectangle_tri(x_range: ArrayLike, y_range: ArrayLike, variant: str = "zigzag"):
    x_range = np.asarray(x_range)
    y_range = np.asarray(y_range)

    nx = len(x_range)
    ny = len(y_range)

    # Create the vertices.
    points = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T

    a = np.arange(nx * ny).reshape(ny, nx).T

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
        idx = np.ones((nx - 1, ny - 1), dtype=bool)
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
        idx = np.ones(((nx - 1), (ny - 1)), dtype=bool)
        idx[: (nx - 1) // 2, : (ny - 1) // 2] = False
        idx[(nx - 1) // 2 :, (ny - 1) // 2 :] = False

        cells = [
            # up
            [c[0][idx], c[1][idx], c[2][idx]],
            [c[0][idx], c[2][idx], c[3][idx]],
            # down
            [c[0][~idx], c[1][~idx], c[3][~idx]],
            [c[1][~idx], c[2][~idx], c[3][~idx]],
        ]

    cells = np.column_stack([np.array(c).reshape(3, -1) for c in cells]).T

    return points, cells
