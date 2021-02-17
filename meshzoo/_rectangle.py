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
    if isinstance(n, int):
        n = (n, n)
    assert isinstance(n, tuple) and len(n) == 2

    nx, ny = n

    xmin, ymin = a0
    xmax, ymax = a1

    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)
    nodes = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T

    a = np.add.outer(np.arange(nx - 1), nx * np.arange(ny - 1))
    elems = np.array([a, a + 1, a + nx + 1, a + nx]).reshape(4, -1).T
    return nodes, elems


def rectangle_tri(
    a0: Tuple[float, float],
    a1: Tuple[float, float],
    n: Union[int, Tuple[int, int]],
    variant: str = "zigzag",
):
    if isinstance(n, int):
        n = (n, n)
    assert isinstance(n, tuple) and len(n) == 2

    # Create the vertices.
    x_range = np.linspace(a0[0], a1[0], n[0])
    y_range = np.linspace(a0[1], a1[1], n[1])
    nodes = np.array(np.meshgrid(x_range, y_range)).reshape(2, -1).T
    elem_fun = {"zigzag": _zigzag, "center": _center, "down": _down, "up": _up}
    return nodes, elem_fun[variant](*n)


def _up(nx, ny):
    # a = [i + j*nx]
    a = np.add.outer(np.arange(nx - 1), nx * np.arange(ny - 1))
    elems0 = np.array([a, a + 1, a + nx + 1]).reshape(3, -1).T
    elems1 = np.array([a, a + 1 + nx, a + nx]).reshape(3, -1).T
    elems = np.concatenate([elems0, elems1])
    return elems


def _down(nx, ny):
    # a = [i + j*nx]
    a = np.add.outer(np.arange(nx - 1), nx * np.arange(ny - 1))
    elems0 = np.array([a, a + 1, a + nx]).reshape(3, -1).T
    elems1 = np.array([a + 1, a + 1 + nx, a + nx]).reshape(3, -1).T
    elems = np.concatenate([elems0, elems1])
    return elems


def _center(nx, ny):
    assert (
        nx % 2 == 1 and ny % 2 == 1
    ), "center mode only works with an odd number of cells"

    # Create the elements (cells).
    # a = [i + j*nx]
    a = np.add.outer(np.arange(nx - 1), nx * np.arange(ny - 1))

    elems = []
    nx2 = (nx - 1) // 2
    ny2 = (ny - 1) // 2

    # bottom left
    ax0 = a[:nx2, :ny2]
    elems.append(np.array([ax0, ax0 + 1, ax0 + nx + 1]).reshape(3, -1).T)
    elems.append(np.array([ax0, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    # bottom right
    ax0 = a[nx2:, :ny2]
    elems.append(np.array([ax0, ax0 + 1, ax0 + nx]).reshape(3, -1).T)
    elems.append(np.array([ax0 + 1, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    # top left
    ax0 = a[:nx2, ny2:]
    elems.append(np.array([ax0, ax0 + 1, ax0 + nx]).reshape(3, -1).T)
    elems.append(np.array([ax0 + 1, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    # top right
    ax0 = a[nx2:, ny2:]
    elems.append(np.array([ax0, ax0 + 1, ax0 + nx + 1]).reshape(3, -1).T)
    elems.append(np.array([ax0, ax0 + 1 + nx, ax0 + nx]).reshape(3, -1).T)

    elems = np.concatenate(elems)

    return elems


def _zigzag(nx, ny):
    # Create the elements (cells).
    # a = [i + j*nx]
    a = np.add.outer(np.arange(nx - 1), nx * np.arange(ny - 1))

    # [i + j*nx, i+1 + j*nx, i+1 + (j+1)*nx]
    elems0 = np.dstack([a, a + 1, a + nx + 1])
    # [i+1 + j*nx, i+1 + (j+1)*nx, i + (j+1)*nx] for "every other" element
    elems0[0::2, 1::2, 0] += 1
    elems0[1::2, 0::2, 0] += 1
    elems0[0::2, 1::2, 1] += nx
    elems0[1::2, 0::2, 1] += nx
    elems0[0::2, 1::2, 2] -= 1
    elems0[1::2, 0::2, 2] -= 1

    # [i + j*nx, i+1 + (j+1)*nx,  i + (j+1)*nx]
    elems1 = np.dstack([a, a + 1 + nx, a + nx])
    # [i + j*nx, i+1 + j*nx, i + (j+1)*nx] for "every other" element
    elems1[0::2, 1::2, 1] -= nx
    elems1[1::2, 0::2, 1] -= nx

    elems = np.concatenate([elems0.reshape(-1, 3), elems1.reshape(-1, 3)])
    return elems
