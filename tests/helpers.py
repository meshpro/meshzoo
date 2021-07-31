import math

import numpy as np


def is_near_equal(a, b, tol=1.0e-12):
    return np.allclose(a, b, rtol=0.0, atol=tol)


def signed_simplex_volumes(coords, cells):
    assert len(coords.shape) == 2
    assert len(cells.shape) == 2
    assert (
        coords.shape[1] + 1 == cells.shape[1]
    ), "Signed areas only make sense for n-simplices in in nD."

    # bc = coords[:, cells]
    # return np.cross((bc[:, :, 1] - bc[:, :, 0]).T, (bc[:, :, 2] - bc[:, :, 0]).T)

    # https://en.wikipedia.org/wiki/Simplex#Volume
    cp = coords[cells]
    n = coords.shape[1]
    # append ones; this appends a column instead of a row as suggested by
    # wikipedia, but that doesn't change the determinant
    cp1 = np.concatenate([cp, np.ones(cp.shape[:-1] + (1,))], axis=-1)

    sign = -1 if n % 2 == 1 else 1
    return sign * np.linalg.det(cp1) / math.factorial(n)
