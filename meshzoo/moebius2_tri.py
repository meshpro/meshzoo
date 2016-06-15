#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh on a slightly Möbius strip.  The Möbius
strip here deviates slightly from the ordinary geometry in that it is
constructed in such a way that the two halves can be exchanged as to allow
better comparison with the pseudo-Möbius geometry.
'''
import numpy as np
from math import copysign


def create_mesh(
        moebius_index=1  # How many twists are there in the 'paper'?
        ):
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
    u_range = np.linspace(0.0, 2*np.pi, num=nl, endpoint=False)
    v_range = np.linspace(-0.5*width, 0.5*width, num=nw)

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
            # The fundamental difference with the ordinary M'obius band here
            # are the squares.
            # It is also possible to to abs() the respective sines and cosines,
            # but this results in a non-smooth manifold.
            a = v*copysign(np.cos(alpha)**2, np.cos(alpha))
            nodes.append([
                scale * (r + a) * np.cos(u),
                scale * (r + a) * np.sin(u),
                flatness * scale * v*copysign(np.sin(alpha)**2, np.sin(alpha))
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1,  i*nw + j + 1]
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

    return np.array(nodes), np.array(elems)


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('moebius2.e', points, {'triangle': cells})
