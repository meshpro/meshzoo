#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh on a rectangle in the x-y-plane.
'''
import numpy as np


def create_mesh(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        nx=11, ny=11,
        zigzag=False
        ):
    if zigzag:
        return _zigzag(xmin, xmax, ymin, ymax, nx, ny)
    else:
        return _canonical(xmin, xmax, ymin, ymax, nx, ny)


def _canonical(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)
    nodes = np.dstack(np.meshgrid(x_range, y_range, np.array([0.0]))) \
        .reshape(-1, 3)

    # Create the elements (cells).
    # a = [i + j*nx]
    a = np.add.outer(np.array(range(nx - 1)), nx * np.array(range(ny - 1)))
    elems0 = np.dstack([a, a + 1, a + nx + 1]).reshape(-1, 3)
    elems1 = np.dstack([a, a + 1 + nx, a + nx]).reshape(-1, 3)
    elems = np.vstack([elems0, elems1])

    return nodes, elems


def _zigzag(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)
    nodes = np.dstack(np.meshgrid(x_range, y_range, np.array([0.0]))) \
        .reshape(-1, 3)

    # Create the elements (cells).
    # a = [i + j*nx]
    a = np.add.outer(np.array(range(nx - 1)), nx * np.array(range(ny - 1)))
    elems = []
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

    elems = np.vstack([
        elems0.reshape(-1, 3), elems1.reshape(-1, 3)
        ])

    return nodes, elems


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('rectangle.vtu', points, {'triangle': cells})
