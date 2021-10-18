import numpy as np

from ._helpers import _compose_from_faces
from ._rectangle import rectangle_quad


def disk(p: int, n: int, offset: float = np.pi / 2):
    x = np.linspace(offset, offset + 2 * np.pi, p, endpoint=False)
    corners = np.vstack(
        [
            [[0.0, 0.0]],
            np.array([np.cos(x), np.sin(x)]).T,
        ]
    )
    faces = [(0, k + 1, k + 2) for k in range(p - 1)] + [(0, p, 1)]

    def edge_adjust(edge, verts):
        if 0 in edge:
            return verts
        dist = np.sqrt(np.einsum("ij,ij->i", verts, verts))
        return verts / dist[:, None]

    def face_adjust(face, bary, verts, corner_verts):
        assert face[0] == 0
        z = np.zeros_like(bary[1])
        edge_proj_bary = np.array([z, bary[1], bary[2]]) / (bary[1] + bary[2])
        edge_proj_cart = np.dot(corner_verts.T, edge_proj_bary).T
        dist = np.sqrt(np.einsum("ij,ij->i", edge_proj_cart, edge_proj_cart))
        return verts / dist[:, None]

    return _compose_from_faces(
        corners, faces, n, edge_adjust=edge_adjust, face_adjust=face_adjust
    )


def disk_quad(n: int):
    a = 1 / np.sqrt(2)
    nodes, cells = rectangle_quad(np.linspace(-a, a, n + 1), np.linspace(-a, a, n + 1))

    # Inflate the nodes towards the circle boundary.
    # Inflate each point such that the 2-norm of the new point is the max-norm of the
    # old.
    alpha = np.max(np.abs(nodes), axis=1)
    beta = np.linalg.norm(nodes, axis=1)
    idx = beta > 1.0e-13
    nodes[idx] = (nodes[idx].T * (alpha[idx] / beta[idx])).T

    return nodes, cells
