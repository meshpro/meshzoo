import meshpy.triangle
import numpy as np


def create_mesh(max_area=1.0):
    # dimensions of the rectangle
    cc_radius = 15.0  # circumcircle radius
    lx = np.sqrt(2.0) * cc_radius
    ly = lx

    h_radius = 1.0

    # corner points
    boundary_points = [
        (0.5 * lx, 0.0),
        (0.5 * lx, 0.5 * ly),
        (-0.5 * lx, 0.5 * ly),
        (-0.5 * lx, -0.5 * ly),
        (0.5 * lx, -0.5 * ly),
        (0.5 * lx, 0.0),
    ]
    # create circular boundary on the inside
    segments = 100
    for k in range(segments + 1):
        angle = k * 2.0 * np.pi / segments
        boundary_points.append((h_radius * np.cos(angle), h_radius * np.sin(angle)))
    # mark the hole by an interior point
    holes = [(0, 0)]

    info = meshpy.triangle.MeshInfo()
    info.set_points(boundary_points)
    info.set_holes(holes)

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
    meshio.write("rectangle_with_hole.e", points, {"triangle": cells})
