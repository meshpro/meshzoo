#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import refine


def create_mesh(ref_steps=2):

    # Circumcircle radius of the triangle.
    cc_radius = 5.0

    # Create initial nodes/elements.
    nodes = cc_radius * np.array([
        np.array([0.0, 1.0, 0.0]),
        np.array([-0.5*np.sqrt(3.0), -0.5, 0.0]),
        np.array([0.5*np.sqrt(3.0), -0.5, 0.0])
        ])
    edges = np.array([
        np.array([0, 1]),
        np.array([0, 2]),
        np.array([1, 2])
        ])
    cells_nodes = np.array([[0, 1, 2]], dtype=int)
    cells_edges = np.array([[0, 1, 2]], dtype=int)

    # Refine.
    for k in range(ref_steps):
        nodes, edges, cells_nodes, cells_edges = \
            refine.refine(nodes, edges, cells_nodes, cells_edges)

    return nodes, cells_nodes


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('triangle.e', points, {'triangle': cells})
