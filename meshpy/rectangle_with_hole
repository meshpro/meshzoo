#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh on a rectangle in the x-y-plane.
'''
from mesh import mesh, magnetic_vector_potentials, meshpy_interface
import numpy as np
import time
# ==============================================================================
def _main():

    # get the file name to be written to
    args = _parse_options()

    # dimensions of the rectangle
    cc_radius = 15.0 # circumcircle radius
    lx = np.sqrt(2.0) * cc_radius
    l = [lx, lx]

    h_radius = 1.0

    # create the mesh data structure
    print 'Create mesh...',
    start = time.time()
    # corner points
    points = [( 0.5*l[0],  0.0 ),
              ( 0.5*l[0],  0.5*l[1]),
              (-0.5*l[0],  0.5*l[1]),
              (-0.5*l[0], -0.5*l[1]),
              ( 0.5*l[0], -0.5*l[1]),
              ( 0.5*l[0],  0.0 )
              ]
    # create circular boundary on the inside
    segments = 100
    for k in xrange(segments+1):
        angle = k * 2.0 * np.pi / segments
        points.append((h_radius * np.cos(angle), h_radius * np.sin(angle)))
    # mark the hole by an interior point
    holes = [(0,0)]
    #holes = None
    mymesh = meshpy_interface.create_mesh(args.maxarea, points, holes=holes)
    elapsed = time.time() - start
    print 'done. (%gs)' % elapsed

    num_nodes = len(mymesh.nodes)
    print '\n%d nodes, %d elements\n' % (num_nodes, len(mymesh.cells))


    # write the mesh
    print 'Write mesh...',
    start = time.time()
    mymesh.write( args.filename )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    return
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser( description = 'Construct a triangulation of a rectangle with a circular hole.' )


    parser.add_argument( 'filename',
                         metavar = 'FILE',
                         type    = str,
                         help    = 'file to be written to'
                       )

    parser.add_argument( '--maxarea', '-m',
                         metavar = 'MAXAREA',
                         dest='maxarea',
                         nargs='?',
                         type=float,
                         const=1.0,
                         default=1.0,
                         help='maximum triangle area (default: 1.0)'
                       )

    return parser.parse_args()
# ==============================================================================
if __name__ == "__main__":
    _main()
# ==============================================================================
