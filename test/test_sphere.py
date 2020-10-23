import numpy
from helpers import _near_equal

import meshzoo


def _compute_cells_normals_dir(points, cells):
    pc = points[cells]
    midpoints = numpy.sum(pc, axis=1) / 3.0
    nrm = numpy.sqrt(numpy.einsum("ij,ij->i", midpoints, midpoints))
    normals = (midpoints.T / nrm).T
    cross = numpy.cross(
        pc[:, 1, :] - pc[:, 0, :],
        pc[:, 2, :] - pc[:, 0, :],
    )
    return numpy.einsum("ij,ij->i", normals, cross)


def test_uv_sphere(num_points_per_circle=20, num_circles=10):
    points, cells = meshzoo.uv_sphere(num_points_per_circle, num_circles)
    assert len(points) == 162
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 320
    assert (_compute_cells_normals_dir(points, cells) > 0.0).all()


def test_tetra_sphere(n=16):
    points, cells = meshzoo.tetra_sphere(n)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert points.shape[1] == 514
    assert _near_equal(numpy.sum(points, axis=1), [0.0, 0.0, 0.0])
    assert len(cells) == 1024
    assert (_compute_cells_normals_dir(points.T, cells) > 0.0).all()


def test_octa_sphere(n=16):
    points, cells = meshzoo.octa_sphere(n)
    assert points.shape[1] == 1026
    assert _near_equal(numpy.sum(points, axis=1), [0.0, 0.0, 0.0])
    assert len(cells) == 2048
    assert (_compute_cells_normals_dir(points.T, cells) > 0.0).all()


def test_icosa_sphere(n=16):
    points, cells = meshzoo.icosa_sphere(n)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert points.shape[1] == 2562
    assert _near_equal(numpy.sum(points, axis=1), [0.0, 0.0, 0.0])
    assert len(cells) == 5120
    assert (_compute_cells_normals_dir(points.T, cells) > 0.0).all()


if __name__ == "__main__":
    test_icosa_sphere()
