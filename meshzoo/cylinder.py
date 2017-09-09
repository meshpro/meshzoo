# -*- coding: utf-8 -*-
#
import numpy


def cylinder():
    # The width of the strip
    width = 1.0

    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 100
    # Number of nodes along the width of the strip (>= 2)
    nw = 10

    # Generate suitable ranges for parametrization
    u_range = numpy.arange(nl, dtype='d') \
        * 2 * numpy.pi \
        / nl
    v_range = numpy.arange(nw, dtype='d') \
        / (nw - 1.0)*width \
        - 0.5 * width

    # Create the vertices. This is based on the parameterization
    # of the M\'obius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    num_nodes = nl * nw
    nodes = numpy.empty(num_nodes, dtype=numpy.dtype((float, 3)))
    k = 0
    for u in u_range:
        for v in v_range:
            nodes[k] = numpy.array([numpy.cos(u), numpy.sin(u), v])
            k += 1

    # create the elements (cells)
    numelems = 2 * nl * (nw-1)
    elems = numpy.zeros([numelems, 3], dtype=int)
    k = 0
    for i in range(nl - 1):
        for j in range(nw - 1):
            elems[k] = [i*nw + j, (i + 1)*nw + j + 1, i * nw + j + 1]
            elems[k+1] = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            k += 2

    # close the geometry
    for j in range(nw - 1):
        elems[k] = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
        elems[k+1] = [(nl - 1)*nw + j, j, j + 1]
        k += 2

    return numpy.array(nodes), numpy.array(elems)
