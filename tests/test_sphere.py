import numpy as np
import pytest

import meshzoo

from .helpers import is_near_equal


def _compute_cells_normals_dir(points, cells):
    pc = points[cells]
    midpoints = np.sum(pc, axis=1) / 3.0
    nrm = np.sqrt(np.einsum("ij,ij->i", midpoints, midpoints))
    normals = (midpoints.T / nrm).T
    cross = np.cross(
        pc[:, 1, :] - pc[:, 0, :],
        pc[:, 2, :] - pc[:, 0, :],
    )
    return np.einsum("ij,ij->i", normals, cross)


def test_uv_sphere(num_points_per_circle=20, num_circles=10):
    points, cells = meshzoo.uv_sphere(num_points_per_circle, num_circles)
    assert len(points) == 162
    assert is_near_equal(np.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 320
    assert (_compute_cells_normals_dir(points, cells) > 0.0).all()
    assert np.all(np.abs(np.einsum("ij,ij->i", points, points) - 1.0) < 1.0e-10)


def test_geo_sphere(num_points_per_circle=20, num_circles=10):
    points, tri, quad = meshzoo.geo_sphere(num_points_per_circle, num_circles)
    # import meshio
    # meshio.write_points_cells("geo-sphere.vtk", points, {"triangle": tri, "quad": quad})
    assert len(points) == 162
    assert is_near_equal(np.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(tri) == 40
    assert len(quad) == 140
    # assert (_compute_cells_normals_dir(points, cells) > 0.0).all()
    assert np.all(np.abs(np.einsum("ij,ij->i", points, points) - 1.0) < 1.0e-10)


def test_tetra_sphere(n=16):
    points, cells = meshzoo.tetra_sphere(n)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert len(points) == 514
    assert is_near_equal(np.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 1024
    assert (_compute_cells_normals_dir(points, cells) > 0.0).all()
    assert np.all(np.abs(np.einsum("ij,ij->i", points, points) - 1.0) < 1.0e-10)


def test_octa_sphere(n=16):
    points, cells = meshzoo.octa_sphere(n)
    assert len(points) == 1026
    assert is_near_equal(np.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 2048
    assert (_compute_cells_normals_dir(points, cells) > 0.0).all()
    assert np.all(np.abs(np.einsum("ij,ij->i", points, points) - 1.0) < 1.0e-10)


@pytest.mark.parametrize("flat_top", [True, False])
def test_icosa_sphere(flat_top, n=16):
    points, cells = meshzoo.icosa_sphere(n, flat_top)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert len(points) == 2562
    assert is_near_equal(np.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 5120
    assert (_compute_cells_normals_dir(points, cells) > 0.0).all()
    assert np.all(np.abs(np.einsum("ij,ij->i", points, points) - 1.0) < 1.0e-10)


if __name__ == "__main__":
    test_geo_sphere()
