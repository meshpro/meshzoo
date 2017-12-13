# -*- coding: utf-8 -*-
#
import numpy


def cylinder(
        width=1.0,  # The width of the strip
        nl=100,  # Number of nodes along the length of the strip
        nw=10,  # Number of nodes along the width of the strip (>= 2)
        ):
    # Generate suitable ranges for parametrization
    u_range = numpy.arange(nl, dtype=float) * 2 * numpy.pi / nl
    v_range = numpy.arange(nw, dtype=float) / (nw - 1.0)*width - 0.5 * width

    # Create the vertices. This is based on the parameterization
    # of the Möbius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = numpy.array([
            [numpy.cos(u), numpy.sin(u), v]
            for u in u_range
            for v in v_range
            ])

    # create the elements (cells)
    elems = numpy.concatenate([
        [
            [i*nw + j, (i + 1)*nw + j + 1, i * nw + j + 1],
            [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1],
        ]
        for i in range(nl - 1)
        for j in range(nw - 1)
        ] + [
        # close the geometry
        [
            [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1],
            [(nl - 1)*nw + j, j, j + 1],
        ]
        for j in range(nw - 1)
        ])

    return nodes, elems
