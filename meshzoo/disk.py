import numpy as np

from .helpers import _compose_from_faces


def disk(p, n, offset=np.pi / 2):
    k = np.arange(p)
    corners = np.vstack(
        [
            [[0.0, 0.0]],
            np.array(
                [
                    np.cos(2 * np.pi * k / p + offset),
                    np.sin(2 * np.pi * k / p + offset),
                ]
            ).T,
        ]
    )
    faces = [(0, k + 1, k + 2) for k in range(p - 1)] + [[0, p, 1]]

    def edge_adjust(edge, verts):
        if 0 in edge:
            return verts
        dist = np.sqrt(np.einsum("ij,ij->i", verts, verts))
        return verts / dist[:, None]

    def face_adjust(face, bary, verts, corner_verts):
        assert face[0] == 0
        edge_proj_bary = np.array([np.zeros(bary.shape[1]), bary[1], bary[2]]) / (
            bary[1] + bary[2]
        )
        edge_proj_cart = np.dot(corner_verts.T, edge_proj_bary).T
        dist = np.sqrt(np.einsum("ij,ij->i", edge_proj_cart, edge_proj_cart))
        return verts / dist[:, None]

    return _compose_from_faces(
        corners, faces, n, edge_adjust=edge_adjust, face_adjust=face_adjust
    )
