import numpy

import meshzoo
from helpers import _near_equal


def test_uv_sphere():
    points, cells = meshzoo.uv_sphere()
    assert len(points) == 162
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 320


def test_iso_sphere(n=8):
    points, cells = meshzoo.iso_sphere(n)
    print(len(points))
    assert len(points) == 2562
    assert _near_equal(numpy.sum(points, axis=0), [0.0, 0.0, 0.0])
    assert len(cells) == 5120

    import meshio
    meshio.write_points_cells("out.vtk", points, {"triangle": cells})


if __name__ == "__main__":
    test_iso_sphere(6)
