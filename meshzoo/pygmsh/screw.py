#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import argparse
import time

import pygmsh as pg
import numpy as np


def create_screw_mesh():

    geom = pg.Geometry()

    # Draw a cross.
    poly = geom.add_polygon([
        [0.0,   0.5, 0.0],
        [-0.1,  0.1, 0.0],
        [-0.5,  0.0, 0.0],
        [-0.1, -0.1, 0.0],
        [0.0,  -0.5, 0.0],
        [0.1,  -0.1, 0.0],
        [0.5,   0.0, 0.0],
        [0.1,   0.1, 0.0]
        ],
        lcar=0.05
        )

    axis = [0, 0, 1]

    geom.extrude(
        'Surface{%s}' % poly,
        translation_axis=axis,
        rotation_axis=axis,
        point_on_axis=[0, 0, 0],
        angle=2.0 / 6.0 * np.pi
        )

    points, cells = pg.generate_mesh(geom)
    return points, cells['tetra']


def _parse_options():
    '''Parse input options.'''
    import argparse
    parser = argparse.ArgumentParser(
        description='Construct tetrahedrization of a toy object.'
        )

    parser.add_argument('filename',
                        metavar='FILE',
                        type=str,
                        help='file to be written to'
                        )

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    import meshio
    args = _parse_options()

    print('Build mesh...')
    start = time.time()
    points, cells = create_screw_mesh()
    elapsed = time.time()-start
    print('done. (%gs)' % elapsed)

    print('\n%d nodes, %d elements' % (len(points), len(cells)))

    print('Write mesh...')
    start = time.time()
    meshio.write(
            args.filename,
            points,
            cells
            )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed
