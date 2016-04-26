#!/usr/bin/env python

import argparse
import meshpy.triangle
import numpy as np
from scipy import special
import time


def create_ellipse_mesh(axes, num_boundary_points):

    # lengths of major and minor axes
    if axes[0] > axes[1]:
        a = axes[0]
        b = axes[1]
    else:
        a = axes[1]
        b = axes[0]

    # Choose the maximum area of a triangle equal to the area of
    # an equilateral triangle on the boundary.
    # For circumference of an ellipse, see
    # http://en.wikipedia.org/wiki/Ellipse#Circumference
    eccentricity = np.sqrt(1.0 - (b/a)**2)
    length_boundary = float(4 * a * special.ellipe(eccentricity))
    a_boundary = length_boundary / num_boundary_points
    max_area = a_boundary**2 * np.sqrt(3) / 4

    # generate points on the circle
    Phi = np.linspace(0, 2*np.pi, num_boundary_points, endpoint=False)
    boundary_points = np.column_stack((a * np.cos(Phi), b * np.sin(Phi)))

    info = meshpy.triangle.MeshInfo()
    info.set_points(boundary_points)

    def _round_trip_connect(start, end):
        result = []
        for i in xrange(start, end):
            result.append((i, i+1))
        result.append((end, start))
        return result
    info.set_facets(_round_trip_connect(0, len(boundary_points)-1))

    def _needs_refinement(vertices, area):
        return bool(area > max_area)

    meshpy_mesh = meshpy.triangle.build(info,
                                        refinement_func=_needs_refinement
                                        )

    # append column
    pts = np.array(meshpy_mesh.points)
    points = np.c_[pts[:, 0], pts[:, 1], np.zeros(len(pts))]

    return points, np.array(meshpy_mesh.elements)


def _parse_options():
    '''Parse input options.'''
    parser = argparse.ArgumentParser(
            description='Construct a triangulation of an ellipse.'
            )

    parser.add_argument('filename',
                        metavar='FILE',
                        type=str,
                        help='file to be written to'
                        )

    parser.add_argument('--num-boundary-points', '-b',
                        default=100,
                        type=int,
                        help='number of nodes on the ellipse boundary'
                        )

    parser.add_argument('--axes', '-a',
                        type=float,
                        nargs=2,
                        default=[1, 0.5],
                        help='axis lengths of the ellipse (default: [10,10])'
                        )

    return parser.parse_args()


if __name__ == '__main__':
    import meshio
    args = _parse_options()

    print('Create mesh...')
    start = time.time()
    points, cells = create_ellipse_mesh(args.axes, args.num_boundary_points)
    elapsed = time.time()-start
    print('done. (%gs)' % elapsed)

    print
    print('%d nodes, %d cells' % (len(points), len(cells)))
    print

    print('Write to file...')
    start = time.time()
    meshio.write(args.filename, points, {'triangle': cells})
    elapsed = time.time()-start
    print('done. (%gs)' % elapsed)
