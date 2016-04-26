#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh the sphere.
'''
import pyfvm
import time
import numpy as np
# ==============================================================================
def _main():

    args = _parse_options()

    nodes = np.array([[ 0.0,  0.0, 1.0],
                      [ 1.0,  0.0, 0.0],
                      [ 0.0,  1.0, 0.0],
                      [-1.0,  0.0, 0.0],
                      [ 0.0, -1.0, 0.0]])
    elems = np.array([[0, 1, 2],
                      [0, 2, 3],
                      [0, 3, 4],
                      [0, 4, 1]])

    # create the mesh data structure
    mymesh = pyfvm.meshTri(nodes, elems)

    # write the mesh
    print 'Writing mesh...',
    start = time.time()
    mymesh.write( args.filename )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    return
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser( description = 'Simple shell.' )

    parser.add_argument('filename',
                        metavar = 'FILE',
                        type    = str,
                        help    = 'file to be written to'
                        )

    return parser.parse_args()
# ==============================================================================
if __name__ == "__main__":
    _main()
# ==============================================================================
