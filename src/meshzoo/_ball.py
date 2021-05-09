import numpy as np

from ._cube import cube_hexa, cube_tetra


def ball_hexa(n):
    a = 1 / np.sqrt(3)
    nodes, elems = cube_hexa((-a, -a, -a), (a, a, a), n)

    # Inflate the nodes towards the circle boundary.
    # Inflate each point such that the 2-norm of the new point is the max-norm of the
    # old.
    alpha = np.max(np.abs(nodes), axis=1)
    beta = np.linalg.norm(nodes, axis=1)
    idx = beta > 1.0e-13
    nodes[idx] = (nodes[idx].T * (alpha[idx] / beta[idx])).T

    return nodes, elems


def ball_tetra(n):
    a = 1 / np.sqrt(3)
    nodes, elems = cube_tetra((-a, -a, -a), (a, a, a), n)

    # Inflate the nodes towards the circle boundary.
    # Inflate each point such that the 2-norm of the new point is the max-norm of the
    # old.
    alpha = np.max(np.abs(nodes), axis=1)
    beta = np.linalg.norm(nodes, axis=1)
    idx = beta > 1.0e-13
    nodes[idx] = (nodes[idx].T * (alpha[idx] / beta[idx])).T

    return nodes, elems
