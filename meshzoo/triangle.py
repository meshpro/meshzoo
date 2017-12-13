# -*- coding: utf-8 -*-
#
import numpy

from .helpers import _refine, create_edges


def triangle(ref_steps=2):
    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    nodes = cc_radius * numpy.array([
        numpy.array([0.0, 1.0, 0.0]),
        numpy.array([-0.5*numpy.sqrt(3.0), -0.5, 0.0]),
        numpy.array([0.5*numpy.sqrt(3.0), -0.5, 0.0])
        ])
    cells_nodes = numpy.array([[0, 1, 2]], dtype=int)

    edge_nodes, cells_edges = create_edges(cells_nodes)

    # Refine.
    args = nodes, cells_nodes, edge_nodes, cells_edges
    for _ in range(ref_steps):
        args = _refine(*args)

    return args[0], args[1]
