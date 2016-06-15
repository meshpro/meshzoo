#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import meshpy.triangle
import numpy as np


def create_mesh(maxarea=1.0):
    # dimensions of the rectangle
    cc_radius = 5.0  # circumcircle radius
    lx = np.sqrt(2.0) * cc_radius
    l = [lx, lx]

    # corner points
    points = [
        (-0.5*l[0], -0.5*l[1]),
        (0.5*l[0], -0.5*l[1]),
        (0.5*l[0], 0.0),
        (0.0, 0.0),
        (0.0, 0.5*l[1]),
        (-0.5*l[0], 0.5*l[1])
        ]

    info = meshpy.triangle.MeshInfo()
    info.set_points(points)

    def _round_trip_connect(start, end):
        result = []
        for i in range(start, end):
            result.append((i, i+1))
        result.append((end, start))
        return result

    info.set_facets(_round_trip_connect(0, len(points)-1))

    def _needs_refinement(vertices, area):
        return bool(area > maxarea)

    meshpy_mesh = meshpy.triangle.build(
            info,
            refinement_func=_needs_refinement
            )

    # append column
    pts = np.array(meshpy_mesh.points)
    points = np.c_[pts[:, 0], pts[:, 1], np.zeros(len(pts))]

    return points, np.array(meshpy_mesh.elements)


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('lshape.e', points, {'triangle': cells})
