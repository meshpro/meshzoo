#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def create_mesh():
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

    # l = 5
    p = 1.5

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
    u_range = np.linspace(0.0, 2*np.pi, num=nl, endpoint=False)
    v_range = np.linspace(-0.5*width, 0.5*width, num=nw)

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
                scale * (r - v * np.cos(alpha)**2) * np.cos(u),
                scale * (r - v * np.cos(alpha)**2) * np.sin(u),
                - flatness * scale * v * np.sin(alpha)**2
                ])

    # create the elements (cells)
    elems = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            elem_nodes = [i*nw + j, (i + 1)*nw + j + 1,  i * nw + j + 1]
            elems.append(elem_nodes)
            elem_nodes = [i*nw + j, (i + 1)*nw + j, (i + 1)*nw + j + 1]
            elems.append(elem_nodes)

    # close the geometry
    for j in range(nw - 1):
        elem_nodes = [(nl - 1)*nw + j, j + 1, (nl - 1)*nw + j + 1]
        elems.append(elem_nodes)
        elem_nodes = [(nl - 1)*nw + j, j, j + 1]
        elems.append(elem_nodes)

    return np.array(nodes), np.array(elems)


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('pseudomoebius.e', points, {'triangle': cells})
