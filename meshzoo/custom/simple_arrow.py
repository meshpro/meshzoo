#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import time


def create_mesh():
    # circumcirlce radius
    cc_radius = 5.0
    lx = 2.0/np.sqrt(3.0) * cc_radius
    l = [lx, lx, lx]

    # create the mesh data structure
    nodes = np.array([[0.0,  0.0, 0.0],
                      [2.0, -1.0, 0.0],
                      [2.0,  1.0, 0.0],
                      [1.0,  0.0, 0.0],
                      [2.0,  0.0, 0.0]])
    cells = np.array([
        [1, 4, 3],
        [1, 3, 0],
        [2, 3, 4],
        [0, 3, 2]
        ])

    return nodes, cells


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('simple_arrow.e', points, {'triangle': cells})
