#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Creates meshes on a cube.
'''
import numpy as np


def create_mesh(ax=1.0, ay=1.0, az=1.0, nx=11, ny=11, nz=11):
    '''Canonical tetrahedrization of the cube.
    Input:
    Edge lenghts of the cube
    Number of nodes along the edges.
    '''
    N = [nx, ny, nz]
    # circumcirlce radius
    cc_radius = 5.0
    lx = 2.0/np.sqrt(3.0) * cc_radius
    l = [ax, ay, az]

    # Generate suitable ranges for parametrization
    x_range = np.linspace(0.0, l[0], N[0])
    y_range = np.linspace(0.0, l[1], N[1])
    z_range = np.linspace(0.0, l[2], N[2])

    # Create the vertices.
    num_nodes = len(x_range) * len(y_range) * len(z_range)
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 3)))
    k = 0
    for x in x_range:
        for y in y_range:
            for z in z_range:
                nodes[k] = np.array([x, y, z])
                k += 1

    # Create the elements (cells).
    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See <http://private.mcnet.ch/baumann/Splitting%20a%20cube%20in%20tetrahedras2.htm>.
    # Also interesting: <http://en.wikipedia.org/wiki/Marching_tetrahedrons>.
    num_cells = 5 * (N[0]-1) * (N[1]-1) * (N[2]-1)
    cellNodes = np.empty(num_cells, dtype=np.dtype((int, 4)))
    l = 0
    for i in range(N[0] - 1):
        for j in range(N[1] - 1):
            for k in range(N[2] - 1):
                # Switch the element styles to make sure the edges match at
                # the faces of the cubes.
                if (i + j + k) % 2 == 0:
                    cellNodes[l] = np.array([
                        N[2] * (N[1]*i     + j  ) + k,
                        N[2] * (N[1]*i     + j+1) + k,
                        N[2] * (N[1]*(i+1) + j  ) + k,
                        N[2] * (N[1]*i     + j  ) + k+1
                        ])
                    l += 1
                    cellNodes[l] = np.array([N[2] * (N[1]*i     + j+1) + k,
                                             N[2] * (N[1]*(i+1) + j+1) + k,
                                             N[2] * (N[1]*(i+1) + j  ) + k,
                                             N[2] * (N[1]*(i+1) + j+1) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * (N[1]*i     + j+1) + k,
                                             N[2] * (N[1]*(i+1) + j  ) + k,
                                             N[2] * (N[1]*i     + j  ) + k+1,
                                             N[2] * (N[1]*(i+1) + j+1) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * (N[1]*i     + j+1) + k,
                                             N[2] * (N[1]*i     + j  ) + k+1,
                                             N[2] * (N[1]*i     + j+1) + k+1,
                                             N[2] * (N[1]*(i+1) + j+1) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * (N[1]*(i+1) + j  ) + k,
                                             N[2] * (N[1]*i     + j  ) + k+1,
                                             N[2] * (N[1]*(i+1) + j+1) + k+1,
                                             N[2] * (N[1]*(i+1) + j  ) + k+1])
                    l += 1
                else:
                    # Like the previous one, but flipped along the first
                    # coordinate: i+1 -> i, i -> i+1.
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*(i+1) + j+1 ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1,
                                             N[2] * ( N[1]*(i+1) + j+1 ) + k+1,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([N[2] * ( N[1]*i     + j   ) + k,
                                             N[2] * ( N[1]*(i+1) + j   ) + k+1,
                                             N[2] * ( N[1]*i     + j+1 ) + k+1,
                                             N[2] * ( N[1]*i     + j   ) + k+1])
                    l += 1

    return nodes, cellNodes


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('cube.e', points, {'tetra': cells})
