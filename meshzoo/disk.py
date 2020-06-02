import meshplex
import numpy

from .triangle import triangle


def tri_disk(n, delaunay=True):
    bary, cells = triangle(n)

    corners = numpy.array(
        [[0.0, -0.5 * numpy.sqrt(3.0), +0.5 * numpy.sqrt(3.0)], [1.0, -0.5, -0.5]]
    )
    points = numpy.dot(corners, bary)

    c = bary.T - [1 / 3, 1 / 3, 1 / 3]
    idx_midpoint = numpy.where(numpy.einsum("ij,ij->i", c, c) < 1.0e-15)[0][0]

    # find the point
    smallest = numpy.argmin(bary, axis=0)
    for k in range(3):
        idx = smallest == k
        # remove the midpoint index to avoid division by 0
        idx[idx_midpoint] = False
        b = bary[:, idx]

        # extrapolate the line [1/3, 1/3, 1/3]-->bary further till bary[k] == 0, i.e.,
        # it sits on the edge.
        # 1/3 + t * (bary[k] - 1/3) == 0
        t = 1 / (1 - 3 * b[k])
        # edge projections
        edge_bary = 1 / 3 + t * (b - 1 / 3)
        edge_points = numpy.dot(corners, edge_bary)
        length = numpy.sqrt(numpy.einsum("ij,ij->j", edge_points, edge_points))
        points[:, idx] = numpy.dot(corners, b / length)

    if delaunay:
        mesh = meshplex.MeshTri(points.T, cells)
        mesh.flip_until_delaunay()
        points = mesh.node_coords
        cells = mesh.cells["nodes"]

    return points, cells
