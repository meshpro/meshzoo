import numpy

from .helpers import _compose_from_faces


def ngon(p, n, offset=numpy.pi / 2):
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
    return _compose_from_faces(corners, faces, n)
