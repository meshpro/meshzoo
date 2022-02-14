import numpy as np

from ._helpers import _compose_from_faces


def tetra_surface(n: int):
    corners = np.array(
        [
            [2 * np.sqrt(2) / 3, 0.0, -1.0 / 3.0],
            [-np.sqrt(2) / 3, np.sqrt(2.0 / 3.0), -1.0 / 3.0],
            [-np.sqrt(2) / 3, -np.sqrt(2.0 / 3.0), -1.0 / 3.0],
            [0.0, 0.0, 1.0],
        ]
    )
    # make sure the normals are pointing outwards
    faces = [(0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3)]

    return _compose_from_faces(corners, faces, n)


def octa_surface(n: int):
    corners = np.array(
        [
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ]
    )
    faces = [
        (0, 2, 4),
        (1, 4, 2),
        (1, 3, 4),
        (0, 4, 3),
        (0, 5, 2),
        (1, 2, 5),
        (1, 5, 3),
        (0, 3, 5),
    ]
    return _compose_from_faces(corners, faces, n)


def icosa_surface(n: int, flat_top: bool = False):
    assert n >= 1
    # Start off with an isosahedron and refine.

    # Construction from
    # <http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html>.
    # Create 12 vertices of a icosahedron.
    t = (1.0 + np.sqrt(5.0)) / 2.0

    if flat_top:
        # This is basically a rotation of the "pointy-top" variant below; more
        # precisely a rotation of theta around [0, 1, 0].
        #
        # theta = np.arctan((t - 1) / t)
        cos_theta = t / np.sqrt(t**2 + (t - 1) ** 2)
        sin_theta = (t - 1) / np.sqrt(t**2 + (t - 1) ** 2)

        corners = np.array(
            [
                [-cos_theta, +t, +sin_theta],
                [+cos_theta, +t, -sin_theta],
                [-cos_theta, -t, +sin_theta],
                [+cos_theta, -t, -sin_theta],
                #
                [+t * sin_theta, -1, +t * cos_theta],
                [+t * sin_theta, +1, +t * cos_theta],
                [-t * sin_theta, -1, -t * cos_theta],
                [-t * sin_theta, +1, -t * cos_theta],
                #
                [+t * cos_theta - sin_theta, 0, -cos_theta - t * sin_theta],
                [+t * cos_theta + sin_theta, 0, +cos_theta - t * sin_theta],
                [-t * cos_theta - sin_theta, 0, -cos_theta + t * sin_theta],
                [-t * cos_theta + sin_theta, 0, +cos_theta + t * sin_theta],
            ]
        )
    else:
        corners = np.array(
            [
                [-1, +t, +0],
                [+1, +t, +0],
                [-1, -t, +0],
                [+1, -t, +0],
                #
                [+0, -1, +t],
                [+0, +1, +t],
                [+0, -1, -t],
                [+0, +1, -t],
                #
                [+t, +0, -1],
                [+t, +0, +1],
                [-t, +0, -1],
                [-t, +0, +1],
            ]
        )

    faces = [
        (0, 11, 5),
        (0, 5, 1),
        (0, 1, 7),
        (0, 7, 10),
        (0, 10, 11),
        (1, 5, 9),
        (5, 11, 4),
        (11, 10, 2),
        (10, 7, 6),
        (7, 1, 8),
        (3, 9, 4),
        (3, 4, 2),
        (3, 2, 6),
        (3, 6, 8),
        (3, 8, 9),
        (4, 9, 5),
        (2, 4, 11),
        (6, 2, 10),
        (8, 6, 7),
        (9, 8, 1),
    ]

    return _compose_from_faces(corners, faces, n)
