#!/usr/bin/env python

import meshpy.triangle
import numpy as np
from scipy import special


def create_mesh(axis0=1, axis1=0.5, num_boundary_points=100):
    # lengths of major and minor axes
    a = max(axis0, axis1)
    b = min(axis0, axis1)

    # Choose the maximum area of a triangle equal to the area of
    # an equilateral triangle on the boundary.
    # For circumference of an ellipse, see
    # https://en.wikipedia.org/wiki/Ellipse#Circumference
    eccentricity = np.sqrt(1.0 - (b / a) ** 2)
    length_boundary = float(4 * a * special.ellipe(eccentricity))
    a_boundary = length_boundary / num_boundary_points
    max_area = a_boundary**2 * np.sqrt(3) / 4

    # generate points on the circle
    Phi = np.linspace(0, 2 * np.pi, num_boundary_points, endpoint=False)
    boundary_points = np.column_stack((a * np.cos(Phi), b * np.sin(Phi)))

    info = meshpy.triangle.MeshInfo()
    info.set_points(boundary_points)

    def _round_trip_connect(start, end):
        result = []
        for i in range(start, end):
            result.append((i, i + 1))
        result.append((end, start))
        return result

    info.set_facets(_round_trip_connect(0, len(boundary_points) - 1))

    def _needs_refinement(vertices, area):
        return bool(area > max_area)

    meshpy_mesh = meshpy.triangle.build(info, refinement_func=_needs_refinement)

    # append column
    pts = np.array(meshpy_mesh.points)
    points = np.c_[pts[:, 0], pts[:, 1], np.zeros(len(pts))]

    return points, np.array(meshpy_mesh.elements)


if __name__ == "__main__":
    import meshio

    points, cells = create_mesh()
    meshio.write("ellipse.e", points, {"triangle": cells})
