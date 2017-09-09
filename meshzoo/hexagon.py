# -*- coding: utf-8 -*-
#
import numpy

from .helpers import _refine


def hexagon(ref_steps=4):
    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    tilt = 0.0
    num_nodes = 7
    nodes = numpy.empty(num_nodes, dtype=numpy.dtype((float, 3)))
    nodes[0] = numpy.array([0.0, 0.0, 0.0])
    for k in range(6):
        phi = (tilt + k/3.0) * numpy.pi
        nodes[k+1] = cc_radius * numpy.array([
            numpy.cos(phi),
            numpy.sin(phi),
            0.0
            ])

    edges = numpy.array([
        numpy.array([0, 1]),
        numpy.array([0, 2]),
        numpy.array([0, 3]),
        numpy.array([0, 4]),
        numpy.array([0, 5]),
        numpy.array([0, 6]),
        numpy.array([1, 2]),
        numpy.array([2, 3]),
        numpy.array([3, 4]),
        numpy.array([4, 5]),
        numpy.array([5, 6]),
        numpy.array([6, 1])
        ])

    cells_nodes = numpy.array([
        numpy.array([0, 1, 2]),
        numpy.array([0, 2, 3]),
        numpy.array([0, 3, 4]),
        numpy.array([0, 4, 5]),
        numpy.array([0, 5, 6]),
        numpy.array([0, 6, 1])
        ])
    cells_edges = numpy.array([
        numpy.array([0, 6, 1]),
        numpy.array([1, 7, 2]),
        numpy.array([2, 8, 3]),
        numpy.array([3, 9, 4]),
        numpy.array([4, 10, 5]),
        numpy.array([5, 11, 0])
        ])

    # Refine.
    for k in range(ref_steps):
        nodes, edges, cells_nodes, cells_edges = \
            _refine(nodes, edges, cells_nodes, cells_edges)

    return nodes, cells_nodes
