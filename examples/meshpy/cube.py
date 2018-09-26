#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Creates meshes on a cube.
"""
import meshpy.tet
import numpy as np


def create_mesh(maxvol=0.1):
    # get the file name to be written to

    # circumcirlce radius
    cc_radius = 5.0
    lx = 2.0 / np.sqrt(3.0) * cc_radius
    l = [lx, lx, lx]

    # Corner points of the cube
    points = [
        (-0.5 * l[0], -0.5 * l[1], -0.5 * l[2]),
        (0.5 * l[0], -0.5 * l[1], -0.5 * l[2]),
        (0.5 * l[0], 0.5 * l[1], -0.5 * l[2]),
        (-0.5 * l[0], 0.5 * l[1], -0.5 * l[2]),
        (-0.5 * l[0], -0.5 * l[1], 0.5 * l[2]),
        (0.5 * l[0], -0.5 * l[1], 0.5 * l[2]),
        (0.5 * l[0], 0.5 * l[1], 0.5 * l[2]),
        (-0.5 * l[0], 0.5 * l[1], 0.5 * l[2]),
    ]
    facets = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 4, 5, 1],
        [1, 5, 6, 2],
        [2, 6, 7, 3],
        [3, 7, 4, 0],
    ]

    # create the mesh
    info = meshpy.tet.MeshInfo()
    info.set_points(points)
    info.set_facets(facets)
    meshpy_mesh = meshpy.tet.build(info, max_volume=maxvol)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


if __name__ == "__main__":
    import meshio

    points, cells = create_mesh()
    meshio.write("cube.e", points, {"tetra": cells})
