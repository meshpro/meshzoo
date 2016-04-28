#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh for a hollow pyramid.
'''
import numpy as np


def create_mesh():
    nodes = np.array([
        [ 0.0,  0.0, 1.0],
        [ 1.0,  0.0, 0.0],
        [ 0.0,  1.0, 0.0],
        [-1.0,  0.0, 0.0],
        [ 0.0, -1.0, 0.0]
        ])
    elems = np.array([
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 1]
        ])

    return nodes, elems


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('simple_shell.e', points, {'triangle': cells})
