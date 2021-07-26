import numpy as np


def _near_equal(a, b, tol=1.0e-12):
    return np.allclose(a, b, rtol=0.0, atol=tol)


def _get_signed_areas(coords, cells):
    bc = coords[:, cells]
    return np.cross((bc[:, :, 1] - bc[:, :, 0]).T, (bc[:, :, 2] - bc[:, :, 0]).T)


def _get_signed_volumes_tetra(points, cells):
    "Calculate cell volumes of tetrahedrons."

    # extract point no. 0 of all cells and reshape
    p0 = points[cells][:, 0].reshape(len(cells), 1, 3)

    # calculate edge vectors "i" as v[:, i] for all cells
    edges = (points[cells] - np.repeat(p0, 4, axis=1))[:, 1:]

    # evaluate cell volumes by the triple product
    # cyclic permutations lead to identical results (0,1,2), (1,2,0), (2,0,1)
    cell_volumes = (
        np.einsum("...i,...i->...", edges[:, 0], np.cross(edges[:, 1], edges[:, 2])) / 6
    )

    return cell_volumes
