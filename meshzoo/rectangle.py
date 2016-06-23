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
    num_nodes = len(x_range) * len(y_range)
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 2)))
    k = 0
    for x in x_range:
        for y in y_range:
            nodes[k] = np.array([x, y])
            k += 1

    # create the elements (cells)
    num_elems = 2 * (nx-1) * (ny-1)
    elems = np.empty(num_elems, dtype=np.dtype((int, 3)))
    k = 0
    for i in range(nx - 1):
        for j in range(ny - 1):
            elems[k] = np.array([i*ny + j, (i + 1)*ny + j + 1,  i*ny + j + 1])
            k += 1
            elems[k] = np.array([i*ny + j, (i + 1)*ny + j, (i + 1)*ny + j + 1])
            k += 1

    nodes = np.c_[nodes[:, 0], nodes[:, 1], np.zeros(len(nodes))]

    return nodes, elems


def _zigzag(xmin, xmax, ymin, ymax, nx, ny):
    # Create the vertices.
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)

    num_nodes = len(x_range) * len(y_range)
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 2)))
    k = 0
    for x in x_range:
        for y in y_range:
            nodes[k] = np.array([x, y])
            k += 1

    # create the elements (cells)
    num_elems = 2 * (nx-1) * (ny-1)
    elems = np.empty(num_elems, dtype=np.dtype((int, 3)))
    k = 0
    for i in range(nx - 1):
        for j in range(ny - 1):
            if (i+j) % 2 == 0:
                elems[k] = np.array([i*ny + j, (i + 1)*ny + j + 1,  i     *ny + j + 1])
                k += 1
                elems[k] = np.array([i*ny + j, (i + 1)*ny + j    , (i + 1)*ny + j + 1])
                k += 1
            else:
                elems[k] = np.array([i    *ny + j, (i+1)*ny + j  , i*ny + j+1])
                k += 1
                elems[k] = np.array([(i+1)*ny + j, (i+1)*ny + j+1, i*ny + j+1])
                k += 1

    nodes = np.c_[nodes[:, 0], nodes[:, 1], np.zeros(len(nodes))]

    return nodes, elems


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('rectangle.e', points, {'triangle': cells})
