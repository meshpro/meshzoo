import numpy
from numpy import cos, pi, sin

from .helpers import _refine, create_edges


def hexagon(ref_steps=4):
    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    tilt = 0.0
    nodes = cc_radius * numpy.concatenate(
        [
            [[0.0, 0.0, 0.0]],
            [
                [cos((tilt + k / 3.0) * pi), sin((tilt + k / 3.0) * pi), 0.0]
                for k in range(6)
            ],
        ]
    )

    cells_nodes = numpy.array(
        [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 6], [0, 6, 1]]
    )

    edge_nodes, cells_edges = create_edges(cells_nodes)

    # Refine.
    args = nodes, cells_nodes, edge_nodes, cells_edges
    for _ in range(ref_steps):
        args = _refine(*args)

    return args[0], args[1]
