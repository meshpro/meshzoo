import numpy


def triangle(n, corners=None):
    if corners is None:
        corners = [
            [0.0, 1.0],
            [-0.5 * numpy.sqrt(3.0), -0.5],
            [+0.5 * numpy.sqrt(3.0), -0.5],
        ]
    corners = numpy.array(corners)

    # First create the mesh in barycentric coordinates
    bary = (
        1.0
        / n
        * numpy.hstack(
            [[numpy.full(n - i + 1, i), numpy.arange(n - i + 1)] for i in range(n + 1)]
        )
    )
    bary = numpy.array([1.0 - bary[0] - bary[1], bary[1], bary[0]])
    points = numpy.dot(corners.T, bary).T

    cells = []
    k = 0
    for i in range(n):
        for j in range(n - i):
            cells.append([k + j, k + j + 1, k + n - i + j + 1])
        for j in range(n - i - 1):
            cells.append([k + j + 1, k + n - i + j + 2, k + n - i + j + 1])
        k += n - i + 1
    cells = numpy.array(cells)

    return points, cells
