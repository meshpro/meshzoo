#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mesh.mesh2d import Mesh2D

import argparse
import numpy as np
import time


def _main():

    # get the file name to be written to
    args = _parse_options()

    # circumcirlce radius
    cc_radius = 5.0
    lx = 2.0/np.sqrt(3.0) * cc_radius
    l = [lx, lx, lx]

    # create the mesh data structure
    print 'Create mesh...',
    start = time.time()
    num_nodes = 5
    nodes = np.array([[0.0,  0.0, 0.0],
                      [2.0, -1.0, 0.0],
                      [2.0,  1.0, 0.0],
                      [1.0,  0.0, 0.0],
                      [2.0,  0.0, 0.0]])
    cellsNodes = np.array([
        [1, 4, 3],
        [1, 3, 0],
        [2, 3, 4],
        [0, 3, 2]
        ])
    mymesh = Mesh2D(nodes, cellsNodes)
    elapsed = time.time() - start
    print 'done. (%gs)' % elapsed

    print '\n%d nodes, %d elements\n' % (num_nodes, len(mymesh.cellsNodes))

    # write the mesh with data
    print 'Write to file...',
    start = time.time()
    mymesh.write(args.filename)
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    return


def _parse_options():
    '''Parse input options.'''

    parser = argparse.ArgumentParser(
        description='Construct a 2D arrow domain (good test case).'
        )

    parser.add_argument(
        'filename',
        metavar='FILE',
        type=str,
        help='file to be written to'
        )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    _main()
