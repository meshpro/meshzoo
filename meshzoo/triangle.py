import numpy


def triangle(n):
    # Create the mesh in barycentric coordinates
    bary = (
        numpy.hstack(
            [[numpy.full(n - i + 1, i), numpy.arange(n - i + 1)] for i in range(n + 1)]
        )
        / n
    )
    bary = numpy.array([1.0 - bary[0] - bary[1], bary[1], bary[0]])

    # Some applications rely on the fact that not values like -1.4125e-16 appear.
    bary[bary < 0.0] = 0.0
    bary[bary > 1.0] = 1.0

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
