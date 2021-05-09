import numpy as np

from ._helpers import _compose_from_faces


def ngon(p: int, n: int, offset: float = np.pi / 2):
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
    faces = [(0, k + 1, k + 2) for k in range(p - 1)] + [(0, p, 1)]
    return _compose_from_faces(corners, faces, n)
