import math

import numpy

from .helpers import _compose_from_faces
from .rectangle import rectangle


def quad_disk(n):
    sqrt12 = math.sqrt(0.5)
    points, cells = rectangle(
        xmin=-sqrt12,
        xmax=+sqrt12,
        ymin=-sqrt12,
        ymax=+sqrt12,
        nx=n,
        ny=n,
        variant="center",
    )

    points = points.T

    # right
    idx = (points[0] + points[1] > 0) & (points[0] - points[1] > 0)
    # extrapolate the line [0, 0]-->point further till point[0] == sqrt2, i.e., it sits
    # on the edge.
    pt = points[:, idx]
    edge_points = (sqrt12 / pt[0]) * pt
    lengths = numpy.sqrt(numpy.einsum("ij,ij->j", edge_points, edge_points))
    points[:, idx] = pt / lengths

    # top
    idx = (points[0] + points[1] > 0) & (points[0] - points[1] < 0)
    pt = points[:, idx]
    edge_points = (sqrt12 / pt[1]) * pt
    lengths = numpy.sqrt(numpy.einsum("ij,ij->j", edge_points, edge_points))
    points[:, idx] = pt / lengths

    # left
    idx = (points[0] + points[1] < 0) & (points[0] - points[1] < 0)
    pt = points[:, idx]
    edge_points = (-sqrt12 / pt[0]) * pt
    lengths = numpy.sqrt(numpy.einsum("ij,ij->j", edge_points, edge_points))
    points[:, idx] = pt / lengths

    # bottom
    idx = (points[0] + points[1] < 0) & (points[0] - points[1] > 0)
    pt = points[:, idx]
    edge_points = (-sqrt12 / pt[1]) * pt
    lengths = numpy.sqrt(numpy.einsum("ij,ij->j", edge_points, edge_points))
    points[:, idx] = pt / lengths

    return points.T, cells


def ngon_disk(p, n, offset=numpy.pi / 2):
    k = numpy.arange(p)
    corners = numpy.vstack(
        [
            [[0.0, 0.0]],
            numpy.array(
                [
                    numpy.cos(2 * numpy.pi * k / p + offset),
                    numpy.sin(2 * numpy.pi * k / p + offset),
                ]
            ).T,
        ]
    )
    faces = [(0, k + 1, k + 2) for k in range(p - 1)] + [[0, p, 1]]

    def edge_adjust(edge, verts):
        if 0 in edge:
            return verts
        dist = numpy.sqrt(numpy.einsum("ij,ij->i", verts, verts))
        return verts / dist[:, None]

    def face_adjust(face, bary, verts, corner_verts):
        assert face[0] == 0
        edge_proj_bary = numpy.array([numpy.zeros(bary.shape[1]), bary[1], bary[2]]) / (
            bary[1] + bary[2]
        )
        edge_proj_cart = numpy.dot(corner_verts.T, edge_proj_bary).T
        dist = numpy.sqrt(numpy.einsum("ij,ij->i", edge_proj_cart, edge_proj_cart))
        return verts / dist[:, None]

    return _compose_from_faces(
        corners, faces, n, edge_adjust=edge_adjust, face_adjust=face_adjust
    )
