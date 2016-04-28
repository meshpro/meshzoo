#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def create_mesh(width=1.0, n=30, radius=1.0):
    # Number of nodes along the width of the strip (>= 2)
    # Choose it such that we have approximately square boxes.
    nw = int(round(width * n/(2*np.pi*radius)))

    # Generate suitable ranges for parametrization
    u_range = np.linspace(0.0, 2*np.pi, num=n, endpoint=False)
    v_range = np.linspace(-0.5*width, 0.5*width, num=nw)

    # Create the vertices.
    nodes = []
    for u in u_range:
        x = radius * np.cos(u)
        y = radius * np.sin(u)
        for v in v_range:
            nodes.append(np.array([x, y, v]))

    # create the elements (cells)
    elems = []
    for i in range(n - 1):
        for j in range(nw - 1):
            elems.append([i*nw + j, (i + 1)*nw + j + 1, i * nw + j + 1])
            elems.append([i*nw + j, (i + 1)*nw + j,     (i + 1)*nw + j + 1])
    # close the geometry
    for j in range(nw - 1):
        elems.append([(n - 1)*nw + j, j + 1, (n - 1)*nw + j + 1])
        elems.append([(n - 1)*nw + j, j, j + 1])

    return np.array(nodes), np.array(elems)


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('tube.e', points, {'triangle': cells})
