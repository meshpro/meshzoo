#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplistic triangular mesh the sphere.
'''
import numpy as np


def create_mesh(num_points_per_circle=20, num_circles=10, radius=1.0):
    # Mesh parameters
    n_phi = num_points_per_circle
    n_theta = num_circles

    # Generate suitable ranges for parametrization
    phi_range = np.linspace(0.0, 2*np.pi, num=n_phi, endpoint=False)
    theta_range = np.linspace(
            -np.pi/2 + np.pi/(n_theta-1),
            np.pi/2 - np.pi/(n_theta-1),
            num=n_theta - 2
            )

    num_nodes = len(theta_range) * len(phi_range) + 2
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 3)))
    # south pole
    south_pole_index = 0
    k = 0
    nodes[k] = np.array([0.0, 0.0, -1.0])
    k += 1
    # nodes in the circles of latitude (except poles)
    for theta in theta_range:
        for phi in phi_range:
            nodes[k] = np.array([
                np.cos(theta) * np.sin(phi),
                np.cos(theta) * np.cos(phi),
                np.sin(theta)
                ])
            k += 1
    # north pole
    north_pole_index = k
    nodes[k] = np.array([0.0, 0.0, 1.0])

    nodes *= radius

    # create the elements (cells)
    num_elems = 2 * (n_theta-2) * n_phi
    elems = np.empty(num_elems, dtype=np.dtype((int, 3)))
    k = 0

    # connections to south pole
    for i in xrange(n_phi - 1):
        elems[k] = np.array([south_pole_index, i+1, i+2])
        k += 1
    # close geometry
    elems[k] = np.array([south_pole_index, n_phi, 1])
    k += 1

    # non-pole elements
    for i in xrange(n_theta - 3):
        for j in xrange(n_phi - 1):
            elems[k] = np.array([
                i*n_phi + j+1,
                i*n_phi + j+2,
                (i+1)*n_phi + j+2
                ])
            k += 1
            elems[k] = np.array([
                i*n_phi + j+1,
                (i+1)*n_phi + j+2,
                (i+1)*n_phi + j + 1
                ])
            k += 1

    # close the geometry
    for i in xrange(n_theta - 3):
        elems[k] = np.array([(i+1)*n_phi, i*n_phi + 1, (i+1)*n_phi + 1])
        k += 1
        elems[k] = np.array([(i+1)*n_phi, (i+1)*n_phi + 1, (i+2)*n_phi])
        k += 1

    # connections to the north pole
    for i in range(n_phi - 1):
        elems[k] = np.array([
            i+1 + n_phi*(n_theta-3) + 1,
            i + n_phi*(n_theta-3) + 1,
            north_pole_index
            ])
        k += 1
    # close geometry
    elems[k] = np.array([
        0 + n_phi*(n_theta-3) + 1,
        n_phi-1 + n_phi*(n_theta-3) + 1,
        north_pole_index
        ])
    k += 1
    assert k == num_elems, 'Wrong element count.'

    return nodes, elems


if __name__ == '__main__':
    import meshio
    points, cells = create_mesh()
    meshio.write('sphere.vtu', points, {'triangle': cells})
