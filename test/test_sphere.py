import numpy

import meshzoo
from helpers import _near_equal


def test_uv_sphere():
    points, cells = meshzoo.uv_sphere()
    assert len(points) == 162
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 320


def test_iso_sphere(n=16):
    points, cells = meshzoo.iso_sphere(n)
    # import meshio
    # meshio.write_points_cells("out.vtk", points, {"triangle": cells})
    assert len(points) == 2562
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 5120


if __name__ == "__main__":
    test_iso_sphere(10)
