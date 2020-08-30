"""
Creates a mesh on a rectangle in the x-y-plane.
"""
import meshpy.triangle
import numpy as np


def create_mesh(edgelength=1.0, max_area=0.01):
    # dimensions of the rectangle
    lx = edgelength
    ly = edgelength

    # corner points
    boundary_points = [
        (-0.5 * lx, -0.5 * ly),
        (0.5 * lx, -0.5 * ly),
        (0.5 * lx, 0.5 * ly),
        (-0.5 * lx, 0.5 * ly),
    ]

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
    meshio.write("rectangle.e", points, {"triangle": cells})
