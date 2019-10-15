import numpy


def simple_arrow():
    # create the mesh data structure
    nodes = numpy.array(
        [
            [0.0, +0.0, 0.0],
            [2.0, -1.0, 0.0],
            [2.0, +1.0, 0.0],
            [1.0, +0.0, 0.0],
            [2.0, +0.0, 0.0],
        ]
    )
    cells = numpy.array([[1, 4, 3], [1, 3, 0], [2, 3, 4], [0, 3, 2]])
    return nodes, cells
