# -*- coding: utf-8 -*-
#
from math import copysign
import numpy


# pylint: disable=too-many-locals
def moebius(
        moebius_index=1  # How many twists are there in the 'paper'?
        ):
    '''Creates a simplistic triangular mesh on a slightly Möbius strip. The
    Möbius strip here deviates slightly from the ordinary geometry in that it
    is constructed in such a way that the two halves can be exchanged to allow
    better comparison with the pseudo-Möbius geometry.
    '''
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 31

    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning Möbius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip.
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the Möbius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        # if u > pi:
        #     pre_alpha = pi / 2 * abs(u/pi - 1)**l + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * abs(u/pi - 1)**l + pi / 2
        # else:
        #     pre_alpha = pi / 2
        # if u > pi:
        #     pre_alpha = pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # else:
        #     pre_alpha = pi / 2
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            # The fundamental difference with the ordinary Möbius band here are
            # the squares.
            # It is also possible to to abs() the respective sines and cosines,
            # but this results in a non-smooth manifold.
            a = v*copysign(numpy.cos(alpha)**2, numpy.cos(alpha))
            nodes.append([
                (r + a) * numpy.cos(u),
                (r + a) * numpy.sin(u),
                flatness * v * copysign(numpy.sin(alpha)**2, numpy.sin(alpha))
                ])
    nodes = scale * numpy.array(nodes)

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1, i*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            elems.append(elem_nodes)

    # close the geometry
    if moebius_index % 2 == 0:
        # Close the geometry upside up (even Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [(nl - 1)*nw + j, j, j + 1]
            elems.append(elem_nodes)
    else:
        # Close the geometry upside down (odd Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1]
            elems.append(elem_nodes)
            elem_nodes = [(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)]
            elems.append(elem_nodes)

    return numpy.array(nodes), numpy.array(elems)


def moebius2(
        moebius_index=1  # How many twists are there in the 'paper'?
        ):
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 30

    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning Möbius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices.
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            if numpy.cos(alpha) > 0:
                c = numpy.cos(alpha)**2
            else:
                c = -numpy.cos(alpha)**2
            if numpy.sin(alpha) > 0:
                s = numpy.sin(alpha)**2
            else:
                s = -numpy.sin(alpha)**2
            nodes.append([
                scale * (r + v*c) * numpy.cos(u),
                scale * (r + v*c) * numpy.sin(u),
                scale * flatness * v*s
               ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1, i*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            elems.append(elem_nodes)
    # close the geometry
    if moebius_index % 2 == 0:
        # Close the geometry upside up (even Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [(nl - 1)*nw + j, j, j + 1]
            elems.append(elem_nodes)
    else:
        # Close the geometry upside down (odd Möbius fold)
        for j in range(nw - 1):
            elem_nodes = [(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1]
            elems.append(elem_nodes)
            elem_nodes = [(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)]
            elems.append(elem_nodes)

    # create the mesh
    return numpy.array(nodes), numpy.array(elems)


def moebius3(
        nl=51,  # Number of nodes along the length of the strip
        nw=11,  # Number of nodes along the width of the strip (>= 2)
        index=1
        ):
    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning M\'obius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the M\'obius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        # if u > pi:
        #     pre_alpha = pi / 2 * abs(u/pi -1)**l + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * abs(u/pi -1)**l + pi / 2
        # else:
        #     pre_alpha = pi / 2
        # if u > pi:
        #     pre_alpha = pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * (1 - (1-abs(u/pi-1)**p)**(1/p)) + pi / 2
        # else:
        #     pre_alpha = pi / 2
        alpha = index * pre_alpha + alpha0
        for v in v_range:
            nodes.append([
                scale * (r + v*numpy.cos(alpha)) * numpy.cos(u),
                scale * (r + v*numpy.cos(alpha)) * numpy.sin(u),
                flatness * scale * v*numpy.sin(alpha)
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elems.append([i*nw + j, (i + 1)*nw + j + 1, i*nw + j + 1])
            elems.append([i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1])
    # close the geometry
    if index % 2 == 0:
        # Close the geometry upside up (even M\'obius fold)
        for j in range(nw - 1):
            elems.append([(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1])
            elems.append([(nl - 1)*nw + j, j, j + 1])
    else:
        # Close the geometry upside down (odd M\'obius fold)
        for j in range(nw - 1):
            elems.append([(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1])
            elems.append([(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)])

    return numpy.array(nodes), numpy.array(elems)


def pseudomoebius():
    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 190
    # Number of nodes along the width of the strip (>= 2)
    nw = 31

    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning M\'obius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # How many twists are there in the 'paper'?
    moebius_index = 1

    # Generate suitable ranges for parametrization
    u_range = numpy.linspace(0.0, 2*numpy.pi, num=nl, endpoint=False)
    v_range = numpy.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the Möbius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        # if u > pi:
        #     pre_alpha = pi / 2 * abs( u/pi -1 )**l + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * abs( u/pi -1 )**l + pi / 2
        # else:
        #     pre_alpha = pi / 2
        # if u > pi:
        #     pre_alpha = pi / 2 * ( 1 - (1-abs(u/pi-1)**p)**(1/p) ) + pi / 2
        # elif u < pi:
        #     pre_alpha = - pi / 2 * ( 1 - (1-abs(u/pi-1)**p)**(1/p) ) + pi / 2
        # else:
        #     pre_alpha = pi / 2
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            # The fundamental difference with the ordinary M'obius band here
            # are the squares.
            # It is also possible to to abs() the respective sines and cosines,
            # but this results in a non-smooth manifold.
            nodes.append([
                scale * (r - v * numpy.cos(alpha)**2) * numpy.cos(u),
                scale * (r - v * numpy.cos(alpha)**2) * numpy.sin(u),
                - flatness * scale * v * numpy.sin(alpha)**2
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1, i * nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            elems.append(elem_nodes)

    # close the geometry
    for j in range(nw - 1):
        elem_nodes = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
        elems.append(elem_nodes)
        elem_nodes = [(nl - 1)*nw + j, j, j + 1]
        elems.append(elem_nodes)

    return numpy.array(nodes), numpy.array(elems)
