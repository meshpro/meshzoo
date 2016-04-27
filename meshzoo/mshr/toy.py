#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import argparse
import time

import dolfin
import mshr


def create_toy_mesh():

    box = mshr.Box(dolfin.Point(-3, -1, -0.5), dolfin.Point(3, 1, 0.5))

    c1 = mshr.Cylinder(dolfin.Point(0, 0, -2), dolfin.Point(0, 0, 2), 0.6, 0.6)
    b1 = mshr.Box(dolfin.Point(-2.5, -0.5, -2), dolfin.Point(-1.5, 0.5, 2))

    # Doesn't quite work yet, cf.
    # <https://bitbucket.org/fenics-project/mshr/issues/46/extrude-issues>.
    # # "triangle"
    # t1 = mshr.Polygon([
    #         dolfin.Point(2.5, -0.5, 10),
    #         dolfin.Point(2.5,  0.5, 10),
    #         dolfin.Point(1.5, -0.5, 10)
    #         ])
    # g3d = mshr.Extrude2D(t1, -10)

    m = mshr.generate_mesh(box - c1 - b1, 20, "cgal")

    return m.coordinates(), m.cells()


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
    points, cells = create_toy_mesh()
    elapsed = time.time()-start
    print('done. (%gs)' % elapsed)

    print('\n%d nodes, %d elements' % (len(points), len(cells)))

    print('Write mesh...')
    start = time.time()
    meshio.write(
            args.filename,
            points,
            {'tetra': cells}
            )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed
