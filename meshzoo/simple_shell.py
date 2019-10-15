import numpy


def simple_shell():
    nodes = numpy.array(
        [
            [+0.0, +0.0, 1.0],
            [+1.0, +0.0, 0.0],
            [+0.0, +1.0, 0.0],
            [-1.0, +0.0, 0.0],
            [+0.0, -1.0, 0.0],
        ]
    )
    elems = numpy.array([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1]])
    return nodes, elems
