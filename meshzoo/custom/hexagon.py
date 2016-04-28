#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a mesh on a hexahedron in the x-y-plane.
'''
import argparse
import numpy as np
import time

import refine


def create_hexagon_mesh(ref_steps):
    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    tilt = 0.0
    num_nodes = 7
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 3)))
    nodes[0] = np.array([0.0, 0.0, 0.0])
    for k in range(6):
        phi = (tilt + k/3.0) * np.pi
        nodes[k+1] = cc_radius * np.array([np.cos(phi), np.sin(phi), 0])

    edges = np.array([
        np.array([0, 1]),
        np.array([0, 2]),
        np.array([0, 3]),
        np.array([0, 4]),
        np.array([0, 5]),
        np.array([0, 6]),
        np.array([1, 2]),
        np.array([2, 3]),
        np.array([3, 4]),
        np.array([4, 5]),
        np.array([5, 6]),
        np.array([6, 1])
        ])

    cells_nodes = np.array([
        np.array([0, 1, 2]),
        np.array([0, 2, 3]),
        np.array([0, 3, 4]),
        np.array([0, 4, 5]),
        np.array([0, 5, 6]),
        np.array([0, 6, 1])
        ])
    cells_edges = np.array([
        np.array([0, 6, 1]),
        np.array([1, 7, 2]),
        np.array([2, 8, 3]),
        np.array([3, 9, 4]),
        np.array([4, 10, 5]),
        np.array([5, 11, 0])
        ])

    # Refine.
    for k in range(ref_steps):
        nodes, edges, cells_nodes, cells_edges = \
            refine.refine(nodes, edges, cells_nodes, cells_edges)

    return nodes, cells_nodes


def _parse_options():
    '''Parse input options.'''
    parser = argparse.ArgumentParser(
            description='Construct triangulation of a hexahedron.'
            )

    parser.add_argument(
            'filename',
            metavar='FILE',
            type=str,
            help='file to be written to'
            )

    parser.add_argument(
            '--refinements', '-r',
            metavar='NUM_REFINEMENTS',
            dest='ref_steps',
            nargs='?',
            type=int,
            default=0,
            help='number of mesh refinement steps to be performed (default: 0)'
            )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    import meshio

    args = _parse_options()

    # create the mesh
    print 'Mesh creation...',
    start = time.time()
    points, cells = create_hexagon_mesh(args.ref_steps)
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    print '\n%d nodes, %d elements' % (len(points), len(cells))

    print 'Write mesh...',
    start = time.time()
    meshio.write(
            args.filename,
            points,
            {'triangle': cells}
            )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed
