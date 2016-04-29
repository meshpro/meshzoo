#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh on a Möbius strip.
'''
import numpy as np


def create_mesh(
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

    # l = 5
    p = 1.5

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning Möbius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = np.linspace(0.0, 2*np.pi, num=nl, endpoint=False)
    v_range = np.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices.
    nodes = []
    for u in u_range:
        pre_alpha = 0.5 * u
        alpha = moebius_index * pre_alpha + alpha0
        for v in v_range:
            if (np.cos(alpha) > 0):
                c = np.cos(alpha)**2
            else:
                c = -np.cos(alpha)**2
            if (np.sin(alpha) > 0):
                s = np.sin(alpha)**2
            else:
                s = -np.sin(alpha)**2
            nodes.append([
                scale * (r + v*c) * np.cos(u),
                scale * (r + v*c) * np.sin(u),
                scale * flatness * v*s
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

    # create the mesh
    return np.array(nodes), np.array(elems)


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('moebius_alt.e', points, {'triangle': cells})
