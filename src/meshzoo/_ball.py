import numpy as np

from ._cube import cube_hexa, cube_tetra


def ball_hexa(n: int):
    a = 1 / np.sqrt(3)
    ls = np.linspace(-a, a, n + 1)
    nodes, cells = cube_hexa(ls, ls, ls)

    # Inflate the nodes towards the circle boundary.
    # Inflate each point such that the 2-norm of the new point is the max-norm of the
    # old.
    alpha = np.max(np.abs(nodes), axis=1)
    beta = np.linalg.norm(nodes, axis=1)
    idx = beta > 1.0e-13
    nodes[idx] = (nodes[idx].T * (alpha[idx] / beta[idx])).T

    return nodes, cells


def ball_tetra(n: int):
    a = 1 / np.sqrt(3)
    ls = np.linspace(-a, a, n + 1)
    nodes, cells = cube_tetra(ls, ls, ls)

    # Inflate the nodes towards the circle boundary.
    # Inflate each point such that the 2-norm of the new point is the max-norm of the
    # old.
    alpha = np.max(np.abs(nodes), axis=1)
    beta = np.linalg.norm(nodes, axis=1)
    idx = beta > 1.0e-13
    nodes[idx] = (nodes[idx].T * (alpha[idx] / beta[idx])).T

    return nodes, cells
