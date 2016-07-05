#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Creates meshes on a cube.
'''
import numpy as np


def create_mesh(
        xmin=0.0, xmax=1.0,
        ymin=0.0, ymax=1.0,
        zmin=0.0, zmax=1.0,
        nx=11, ny=11, nz=11
        ):
    '''Canonical tetrahedrization of the cube.
    Input:
    Edge lenghts of the cube
    Number of nodes along the edges.
    '''
    # Generate suitable ranges for parametrization
    x_range = np.linspace(xmin, xmax, nx)
    y_range = np.linspace(ymin, ymax, ny)
    z_range = np.linspace(zmin, zmax, nz)

    # Create the vertices.
    x, y, z = np.meshgrid(x_range, y_range, z_range, indexing='ij')
    nodes = np.stack([x, y, z]).T.reshape(-1, 3)

    # Create the elements (cells).
    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See <http://private.mcnet.ch/baumann/Splitting%20a%20cube%20in%20tetrahedras2.htm>.
    # Also interesting: <http://en.wikipedia.org/wiki/Marching_tetrahedrons>.
    # Switch the element styles to make sure the edges match at the faces of
    # the cubes.
    elems = []
    elems.append(np.array([
        [
            i   + nx*j     + nx*ny * k,
            i   + nx*(j+1) + nx*ny * k,
            i+1 + nx*j     + nx*ny * k,
            i   + nx*j     + nx*ny * (k+1)
        ]
        for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
        if (i + j + k) % 2 == 0
        ]))
    elems.append(np.array([
        [
            i   + nx*(j+1) + nx*ny * k,
            i+1 + nx*(j+1) + nx*ny * k,
            i+1 + nx*j     + nx*ny * k,
            i+1 + nx*(j+1) + nx*ny * (k+1)
        ]
        for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
        if (i + j + k) % 2 == 0
        ]))
    elems.append(np.array([
        [
            i   + nx*(j+1) + nx*ny * k,
            i+1 + nx*j     + nx*ny * k,
            i   + nx*j     + nx*ny * (k+1),
            i+1 + nx*(j+1) + nx*ny * (k+1)
        ]
        for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
        if (i + j + k) % 2 == 0
        ]))
    elems.append(np.array([
        [
            i   + nx * (j+1) + nx*ny * k,
            i   + nx * j     + nx*ny * (k+1),
            i   + nx * (j+1) + nx*ny * (k+1),
            i+1 + nx * (j+1) + nx*ny * (k+1)
        ]
        for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
        if (i + j + k) % 2 == 0
        ]))
    elems.append(np.array([
        [
            i+1 + nx * j     + nx*ny * k,
            i   + nx * j     + nx*ny * (k+1),
            i+1 + nx * (j+1) + nx*ny * (k+1),
            i+1 + nx * j     + nx*ny * (k+1)
        ]
        for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
        if (i + j + k) % 2 == 0
        ]))
    # Like the previous one, but flipped along the first coordinate: i+1 -> i,
    # i -> i+1.
    if nx + ny + nz > 6:
        elems.append(np.array([
            [
                i+1 + nx * j     + nx*ny * k,
                i+1 + nx * (j+1) + nx*ny * k,
                i   + nx * j     + nx*ny * k,
                i+1 + nx * j     + nx*ny * (k+1)
            ]
            for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
            if (i + j + k) % 2 != 0
            ]))
        elems.append(np.array([
            [
                i+1 + nx * (j+1) + nx*ny * k,
                i   + nx * (j+1) + nx*ny * k,
                i   + nx * j     + nx*ny * k,
                i   + nx * (j+1) + nx*ny * (k+1)
            ]
            for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
            if (i + j + k) % 2 != 0
            ]))
        elems.append(np.array([
            [
                i+1 + nx * (j+1) + nx*ny * k,
                i   + nx * j     + nx*ny * k,
                i+1 + nx * j     + nx*ny * (k+1),
                i   + nx * (j+1) + nx*ny * (k+1)
            ]
            for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
            if (i + j + k) % 2 != 0
            ]))
        elems.append(np.array([
            [
                i+1 + nx * (j+1) + nx*ny * k,
                i+1 + nx * j     + nx*ny * (k+1),
                i+1 + nx * (j+1) + nx*ny * (k+1),
                i   + nx * (j+1) + nx*ny * (k+1)
            ]
            for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
            if (i + j + k) % 2 != 0
            ]))
        elems.append(np.array([
            [
                i   + nx * j     + nx*ny * k,
                i+1 + nx * j     + nx*ny * (k+1),
                i   + nx * (j+1) + nx*ny * (k+1),
                i   + nx * j     + nx*ny * (k+1)
            ]
            for i in range(nx - 1) for j in range(ny - 1) for k in range(nz - 1)
            if (i + j + k) % 2 != 0
            ]))

    elems = np.vstack(elems)

    return nodes, elems


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('cube.vtu', points, {'tetra': cells})
