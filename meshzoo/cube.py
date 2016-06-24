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
    nodes = np.array([
        np.array([x, y, z]) for x in x_range for y in y_range for z in z_range
        ])

    # Create the elements (cells).
    # There is 1 way to split a cube into 5 tetrahedra,
    # and 12 ways to split it into 6 tetrahedra.
    # See <http://private.mcnet.ch/baumann/Splitting%20a%20cube%20in%20tetrahedras2.htm>.
    # Also interesting: <http://en.wikipedia.org/wiki/Marching_tetrahedrons>.
    num_cells = 5 * (nx-1) * (ny-1) * (nz-1)
    cellNodes = np.empty(num_cells, dtype=np.dtype((int, 4)))
    l = 0
    for i in range(nx - 1):
        for j in range(ny - 1):
            for k in range(nz - 1):
                # Switch the element styles to make sure the edges match at
                # the faces of the cubes.
                if (i + j + k) % 2 == 0:
                    cellNodes[l] = np.array([
                        nz * (ny*i     + j  ) + k,
                        nz * (ny*i     + j+1) + k,
                        nz * (ny*(i+1) + j  ) + k,
                        nz * (ny*i     + j  ) + k+1
                        ])
                    l += 1
                    cellNodes[l] = np.array([nz * (ny*i     + j+1) + k,
                                             nz * (ny*(i+1) + j+1) + k,
                                             nz * (ny*(i+1) + j  ) + k,
                                             nz * (ny*(i+1) + j+1) + k+1])
                    l += 1
                    cellNodes[l] = np.array([nz * (ny*i     + j+1) + k,
                                             nz * (ny*(i+1) + j  ) + k,
                                             nz * (ny*i     + j  ) + k+1,
                                             nz * (ny*(i+1) + j+1) + k+1])
                    l += 1
                    cellNodes[l] = np.array([nz * (ny*i     + j+1) + k,
                                             nz * (ny*i     + j  ) + k+1,
                                             nz * (ny*i     + j+1) + k+1,
                                             nz * (ny*(i+1) + j+1) + k+1])
                    l += 1
                    cellNodes[l] = np.array([nz * (ny*(i+1) + j  ) + k,
                                             nz * (ny*i     + j  ) + k+1,
                                             nz * (ny*(i+1) + j+1) + k+1,
                                             nz * (ny*(i+1) + j  ) + k+1])
                    l += 1
                else:
                    # Like the previous one, but flipped along the first
                    # coordinate: i+1 -> i, i -> i+1.
                    cellNodes[l] = np.array([nz * ( ny*(i+1) + j   ) + k,
                                             nz * ( ny*(i+1) + j+1 ) + k,
                                             nz * ( ny*i     + j   ) + k,
                                             nz * ( ny*(i+1) + j   ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([nz * ( ny*(i+1) + j+1 ) + k,
                                             nz * ( ny*i     + j+1 ) + k,
                                             nz * ( ny*i     + j   ) + k,
                                             nz * ( ny*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([nz * ( ny*(i+1) + j+1 ) + k,
                                             nz * ( ny*i     + j   ) + k,
                                             nz * ( ny*(i+1) + j   ) + k+1,
                                             nz * ( ny*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([nz * ( ny*(i+1) + j+1 ) + k,
                                             nz * ( ny*(i+1) + j   ) + k+1,
                                             nz * ( ny*(i+1) + j+1 ) + k+1,
                                             nz * ( ny*i     + j+1 ) + k+1])
                    l += 1
                    cellNodes[l] = np.array([nz * ( ny*i     + j   ) + k,
                                             nz * ( ny*(i+1) + j   ) + k+1,
                                             nz * ( ny*i     + j+1 ) + k+1,
                                             nz * ( ny*i     + j   ) + k+1])
                    l += 1

    return nodes, cellNodes


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('cube.vtu', points, {'tetra': cells})
