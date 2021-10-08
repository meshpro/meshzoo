import numpy as np

from ._helpers import _compose_from_faces


def ngon(p: int, n: int, offset: float = np.pi / 2):
    x = np.linspace(offset, offset + 2 * np.pi, p, endpoint=False)
    corners = np.vstack(
        [
            [[0.0, 0.0]],
            np.array([np.cos(x), np.sin(x)]).T,
        ]
    )
    faces = [(0, k + 1, k + 2) for k in range(p - 1)] + [(0, p, 1)]
    return _compose_from_faces(corners, faces, n)
