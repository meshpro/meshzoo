# -*- coding: utf-8 -*-
#
import numpy

from .helpers import _refine


def triangle(ref_steps=2):
    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    nodes = cc_radius * numpy.array([
        numpy.array([0.0, 1.0, 0.0]),
        numpy.array([-0.5*numpy.sqrt(3.0), -0.5, 0.0]),
        numpy.array([0.5*numpy.sqrt(3.0), -0.5, 0.0])
        ])
    edges = numpy.array([
        numpy.array([0, 1]),
        numpy.array([0, 2]),
        numpy.array([1, 2])
        ])
    cells_nodes = numpy.array([[0, 1, 2]], dtype=int)
    cells_edges = numpy.array([[0, 1, 2]], dtype=int)

    # Refine.
    for _ in range(ref_steps):
        nodes, edges, cells_nodes, cells_edges = \
            _refine(nodes, edges, cells_nodes, cells_edges)

    return nodes, cells_nodes
