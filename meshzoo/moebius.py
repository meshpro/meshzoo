# -*- coding: utf-8 -*-
#
import numpy


# pylint: disable=too-many-locals
def moebius(
        moebius_index=1,  # How many twists are there in the 'paper'?
        nl=190,  # Number of nodes along the length of the strip
        nw=31,  # Number of nodes along the width of the strip (>= 2)
        mode='classical'
        ):
    '''Creates a simplistic triangular mesh on a slightly Möbius strip. The
    Möbius strip here deviates slightly from the ordinary geometry in that it
    is constructed in such a way that the two halves can be exchanged as to
    allow better comparison with the pseudo-Möbius geometry.

    The mode is either `'classical'` or `'smooth'`. The first is the classical
    Möbius band parametrization, the latter a smoothed variant matching
    `'pseudo'`.
    '''
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
    sin_u = numpy.sin(u_range)
    cos_u = numpy.cos(u_range)
    alpha = moebius_index * 0.5*u_range + alpha0
    sin_alpha = numpy.sin(alpha)
    cos_alpha = numpy.cos(alpha)

    if mode == 'classical':
        a = cos_alpha
        b = sin_alpha
        reverse_seam = moebius_index % 2 == 1
    elif mode == 'smooth':
        # The fundamental difference with the ordinary Möbius band here are the
        # squares.
        # It is also possible to to abs() the respective sines and cosines, but
        # this results in a non-smooth manifold.
        a = numpy.copysign(cos_alpha**2, cos_alpha)
        b = numpy.copysign(sin_alpha**2, sin_alpha)
        reverse_seam = moebius_index % 2 == 1
    else:
        assert mode == 'pseudo'
        a = cos_alpha**2
        b = sin_alpha**2
        reverse_seam = False

    nodes = scale * numpy.array([
        numpy.outer(a * cos_u, v_range) + r*cos_u[:, numpy.newaxis],
        numpy.outer(a * sin_u, v_range) + r*sin_u[:, numpy.newaxis],
        numpy.outer(b, v_range) * flatness
        ]).reshape(3, -1).T

    elems = _create_elements(nl, nw, reverse_seam)
    return nodes, elems


def _create_elements(nl, nw, reverse_seam):
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elems.append([i*nw + j, (i + 1)*nw + j + 1, i*nw + j + 1])
            elems.append([i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1])

    # close the geometry
    if reverse_seam:
        # Close the geometry upside down (odd Möbius fold)
        for j in range(nw - 1):
            elems.append([(nl-1)*nw + j, (nw-1) - (j+1), (nl-1)*nw + j+1])
            elems.append([(nl-1)*nw + j, (nw-1) - j, (nw-1) - (j+1)])
    else:
        # Close the geometry upside up (even Möbius fold)
        for j in range(nw - 1):
            elems.append([(nl-1)*nw + j, j + 1, (nl - 1)*nw + j + 1])
            elems.append([(nl-1)*nw + j, j, j + 1])

    return numpy.array(elems)
