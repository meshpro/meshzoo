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
    # dimensions of the rectangle
    if zigzag:
        return _zigzag(xmin, xmax, ymin, ymax, nx, ny)
    else:
        return _canonical(xmin, xmax, ymin, ymax, nx, ny)


def _canonical(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)

    nodes = np.array([
        [x, y, 0.0] for x in x_range for y in y_range
        ])

    # create the elements (cells)
    elems0 = np.array([
        [i*ny + j, (i + 1)*ny + j + 1,  i*ny + j + 1]
        for i in range(nx - 1)
        for j in range(ny - 1)
        ])
    elems1 = np.array([
        [i*ny + j, (i + 1)*ny + j, (i + 1)*ny + j + 1]
        for i in range(nx - 1)
        for j in range(ny - 1)
        ])
    elems = np.vstack([elems0, elems1])

    return nodes, elems


def _zigzag(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)

    nodes = np.array([
        [x, y, 0.0] for x in x_range for y in y_range
        ])

    elems0 = np.array([
        [i*ny + j, (i + 1)*ny + j + 1,  i*ny + j + 1]
        for i in range(nx - 1)
        for j in range(ny - 1)
        if (i+j) % 2 == 0
        ])
    elems1 = np.array([
        [i*ny + j, (i + 1)*ny + j, (i + 1)*ny + j + 1]
        for i in range(nx - 1)
        for j in range(ny - 1)
        if (i+j) % 2 == 0
        ])
    elems2 = np.array([
        [i*ny + j, (i+1)*ny + j, i*ny + j+1]
        for i in range(nx - 1)
        for j in range(ny - 1)
        if (i+j) % 2 != 0
        ])
    elems3 = np.array([
        [(i+1)*ny + j, (i+1)*ny + j+1, i*ny + j+1]
        for i in range(nx - 1)
        for j in range(ny - 1)
        if (i+j) % 2 != 0
        ])
    elems = np.vstack([elems0, elems1, elems2, elems3])

    return nodes, elems


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('rectangle.vtu', points, {'triangle': cells})
