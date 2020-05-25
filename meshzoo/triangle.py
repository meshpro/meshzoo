import numpy


class Tri:
    def __init__(self, bary, cells):
        self.bary = bary
        self.cells = cells

    def points(self, corners=None):
        if corners is None:
            corners = numpy.array(
                [
                    [0.0, 1.0],
                    [-0.5 * numpy.sqrt(3.0), -0.5],
                    [+0.5 * numpy.sqrt(3.0), -0.5],
                ]
            ).T
        corners = numpy.asarray(corners)
        return numpy.dot(corners, self.bary).T


def triangle(n):
    # First create the mesh in barycentric coordinates
    bary = (
        numpy.hstack(
            [[numpy.full(n - i + 1, i), numpy.arange(n - i + 1)] for i in range(n + 1)]
        )
        / n
    )
    bary = numpy.array([1.0 - bary[0] - bary[1], bary[1], bary[0]])

    cells = []
    k = 0
    for i in range(n):
        j = numpy.arange(n - i)
        cells.append(numpy.column_stack([k + j, k + j + 1, k + n - i + j + 1]))
        #
        j = j[:-1]
        cells.append(
            numpy.column_stack([k + j + 1, k + n - i + j + 2, k + n - i + j + 1])
        )
        k += n - i + 1

    cells = numpy.vstack(cells)

    return bary, cells
