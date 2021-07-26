import numpy as np
from helpers import _get_signed_volumes_tetra

import meshzoo


def test_cube():
    points, cells = meshzoo.cube_tetra((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 11)
    assert len(points) == 1331
    assert len(cells) == 5000

    points, cells = meshzoo.cube_tetra((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 3)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 40

    volumes = _get_signed_volumes_tetra(points, cells)

    assert len(volumes) == len(cells)
    assert np.all(np.sign(volumes) == 1)


def test_cube_hexa():
    points, cells = meshzoo.cube_hexa((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 11)
    assert len(points) == 1331
    assert len(cells) == 1000
    # import meshio
    # meshio.Mesh(points, {"hexahedron": cells}).write("cube-hexa.vtk")

    points, cells = meshzoo.cube_hexa((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 3)
    assert len(points) == 27
    assert all(np.sum(points, axis=0) == [13.5, 13.5, 13.5])
    assert len(cells) == 8


if __name__ == "__main__":
    test_cube()
