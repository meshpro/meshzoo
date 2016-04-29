#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh on a rectangle in the x-y-plane.
'''
import numpy as np


def create_mesh(edgelength=1.0, nx=11, zigzag=False):
    # dimensions of the rectangle
    l = [edgelength, edgelength]

    if zigzag:
        return _zigzag(l, [nx, nx])
    else:
        return _canonical(l, [nx, nx])


def _canonical(l, N):
    # Create the vertices.
    x_range = np.linspace(-0.5*l[0], 0.5*l[0], N[0])
    y_range = np.linspace(-0.5*l[1], 0.5*l[1], N[1])
    num_nodes = len(x_range) * len(y_range)
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 2)))
    k = 0
    for x in x_range:
        for y in y_range:
            nodes[k] = np.array([x, y])
            k += 1

    # create the elements (cells)
    num_elems = 2 * (N[0]-1) * (N[1]-1)
    elems = np.empty(num_elems, dtype=np.dtype((int, 3)))
    k = 0
    for i in xrange(N[0] - 1):
        for j in xrange(N[1] - 1):
            elems[k] = np.array([i*N[1] + j, (i + 1)*N[1] + j + 1,  i*N[1] + j + 1])
            k += 1
            elems[k] = np.array([i*N[1] + j, (i + 1)*N[1] + j, (i + 1)*N[1] + j + 1])
            k += 1

    nodes = np.c_[nodes[:, 0], nodes[:, 1], np.zeros(len(nodes))]

    return nodes, elems


def _zigzag(l, N):
    # Create the vertices.
    x_range = np.linspace(-0.5*l[0], 0.5*l[0], N[0])
    y_range = np.linspace(-0.5*l[1], 0.5*l[1], N[1])

    num_nodes = len(x_range) * len(y_range)
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 2)))
    k = 0
    for x in x_range:
        for y in y_range:
            nodes[k] = np.array([x, y])
            k += 1

    # create the elements (cells)
    num_elems = 2 * (N[0]-1) * (N[1]-1)
    elems = np.empty(num_elems, dtype=np.dtype((int, 3)))
    k = 0
    for i in xrange(N[0] - 1):
        for j in xrange(N[1] - 1):
            if (i+j)%2 == 0:
                elems[k] = np.array([i*N[1] + j, (i + 1)*N[1] + j + 1,  i     *N[1] + j + 1])
                k += 1
                elems[k] = np.array([i*N[1] + j, (i + 1)*N[1] + j    , (i + 1)*N[1] + j + 1])
                k += 1
            else:
                elems[k] = np.array([i    *N[1] + j, (i+1)*N[1] + j  , i*N[1] + j+1])
                k += 1
                elems[k] = np.array([(i+1)*N[1] + j, (i+1)*N[1] + j+1, i*N[1] + j+1])
                k += 1

    nodes = np.c_[nodes[:, 0], nodes[:, 1], np.zeros(len(nodes))]

    return nodes, elems


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('rectangle.e', points, {'triangle': cells})
