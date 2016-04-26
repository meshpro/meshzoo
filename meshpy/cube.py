#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
'''
Creates meshes on a cube.
'''
import argparse
import meshio
import meshpy.tet
import numpy as np
import time


def create_cube_mesh(maxvol):
    # get the file name to be written to

    # circumcirlce radius
    cc_radius = 5.0
    lx = 2.0/np.sqrt(3.0) * cc_radius
    l = [lx, lx, lx]

    # Corner points of the cube
    points = [
            (-0.5*l[0], -0.5*l[1], -0.5*l[2]),
            ( 0.5*l[0], -0.5*l[1], -0.5*l[2]),
            ( 0.5*l[0],  0.5*l[1], -0.5*l[2]),
            (-0.5*l[0],  0.5*l[1], -0.5*l[2]),
            (-0.5*l[0], -0.5*l[1],  0.5*l[2]),
            ( 0.5*l[0], -0.5*l[1],  0.5*l[2]),
            ( 0.5*l[0],  0.5*l[1],  0.5*l[2]),
            (-0.5*l[0],  0.5*l[1],  0.5*l[2])
            ]
    facets = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 4, 5, 1],
            [1, 5, 6, 2],
            [2, 6, 7, 3],
            [3, 7, 4, 0]
            ]

    # create the mesh
    info = meshpy.tet.MeshInfo()
    info.set_points(points)
    info.set_facets(facets)
    meshpy_mesh = meshpy.tet.build(info, max_volume=maxvol)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


def _parse_options():
    '''Parse input options.'''

    parser = argparse.ArgumentParser(
        description='Construct a trival tetrahedrization of a cube.'
        )

    parser.add_argument(
        'filename',
        metavar='FILE',
        type=str,
        help='file to be written to'
        )

    parser.add_argument(
        '--maxvol', '-m',
        metavar='MAXVOL',
        dest='maxvol',
        nargs='?',
        type=float,
        const=0.0,
        default=0.1,
        help='meshpy tetrahedrization with MAXVOL maximum tetrahedron volume'
        )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = _parse_options()

    print('Create mesh...')
    start = time.time()
    points, cells = create_cube_mesh(args.maxvol)
    elapsed = time.time() - start
    print 'done. (%gs)' % elapsed

    print '\n%d nodes, %d elements\n' % (len(points), len(cells))

    print('Write mesh...')
    start = time.time()
    meshio.write(
            args.filename,
            points,
            {'tetra': cells}
            )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed
