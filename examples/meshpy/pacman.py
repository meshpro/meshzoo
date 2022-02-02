"""
Creates a mesh for a circle with a cut.
"""
import meshpy.triangle
import numpy as np


def create_pacman_mesh(num_boundary_points=50):
    n_phi = num_boundary_points
    radius = 5.0

    # set those to 0.0 for perfect circle
    cut_angle = 0.1 * 2 * np.pi
    cut_depth = 0.5 * radius

    # Choose the maximum area of a triangle equal to the area of
    # an equilateral triangle on the boundary.
    a_boundary = (2 * np.pi - cut_angle) * radius / n_phi
    max_area = a_boundary**2 * np.sqrt(3.0) / 4.0
    max_area = float(max_area)  # meshpy can't deal with np.float64

    # generate points on the boundary
    Phi = np.linspace(
        0.5 * cut_angle, 2 * np.pi - 0.5 * cut_angle, n_phi, endpoint=False
    )
    boundary_points = []
    if abs(cut_angle) > 0.0 or cut_depth != 0.0:
        boundary_points.append((radius - cut_depth, 0.0))
    for phi in Phi:
        boundary_points.append((radius * np.cos(phi), radius * np.sin(phi)))

    # create the mesh
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

    points, cells = create_pacman_mesh()
    meshio.write("pacman.vtu", points, {"triangle": cells})
