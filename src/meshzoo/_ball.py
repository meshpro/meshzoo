import numpy as np

from ._cube import cube_hexa, cube_tetra
from ._helpers import _cell_volumes_tetra


def ball_hexa(n: int):
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


def ball_tetra(n: int):
    a = 1 / np.sqrt(3)
    nodes, elems = cube_tetra((-a, -a, -a), (a, a, a), n)

    # Inflate the nodes towards the circle boundary.
    # Inflate each point such that the 2-norm of the new point is the max-norm of the
    # old.
    alpha = np.max(np.abs(nodes), axis=1)
    beta = np.linalg.norm(nodes, axis=1)
    idx = beta > 1.0e-13
    nodes[idx] = (nodes[idx].T * (alpha[idx] / beta[idx])).T

    # fix elems with negative volumes
    volumes = _cell_volumes_tetra(nodes, elems)
    elems[volumes < 0] = elems[volumes < 0][:, [0, 2, 1, 3]]

    return nodes, elems
